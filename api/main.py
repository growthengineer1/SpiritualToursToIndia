import os
import secrets
import uuid
from collections import OrderedDict, deque
from contextlib import suppress
from datetime import datetime
import logging
from threading import Lock
from time import monotonic
from typing import Optional

import httpx
import psycopg2
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="Spiritual Tours to India API")
logger = logging.getLogger(__name__)

# The marketing site is hosted separately on Cloudflare Pages.  Keep this
# list explicit: credentialed CORS requests must never use a wildcard origin.
ALLOWED_CORS_ORIGINS = [
    "https://spiritualtourstoindia.com",
    "https://www.spiritualtourstoindia.com",
    # Documented local development servers (see docs/static-site-migration.md).
    "http://localhost:3000",
    "http://localhost:5000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

CLOUDFLARE_WORKER_URL = "https://spiritualtourstoindiaemail.sabin.workers.dev"
EMAIL_RECIPIENTS = ["namaste@smukti.com", "sabin@smukti.com"]
LEAD_RATE_LIMIT = 5
LEAD_RATE_WINDOW_SECONDS = 10 * 60
# Keep this application-layer safeguard bounded. Edge controls remain the
# authoritative protection when multiple API processes are running.
MAX_RATE_LIMIT_CLIENTS = 10_000


class LeadRateLimiter:
    """A small, process-local sliding-window limiter for public submissions."""

    def __init__(self, limit: int, window_seconds: float, max_clients: int):
        self.limit = limit
        self.window_seconds = window_seconds
        self.max_clients = max_clients
        self._submissions: OrderedDict[str, deque[float]] = OrderedDict()
        self._lock = Lock()

    def allow(self, client_id: str, now: Optional[float] = None) -> bool:
        timestamp = monotonic() if now is None else now
        cutoff = timestamp - self.window_seconds
        with self._lock:
            attempts = self._submissions.get(client_id)
            if attempts is None:
                if len(self._submissions) >= self.max_clients:
                    self._submissions.popitem(last=False)
                attempts = deque()
                self._submissions[client_id] = attempts
            else:
                self._submissions.move_to_end(client_id)

            while attempts and attempts[0] <= cutoff:
                attempts.popleft()
            if len(attempts) >= self.limit:
                return False
            attempts.append(timestamp)
            return True


lead_rate_limiter = LeadRateLimiter(
    LEAD_RATE_LIMIT, LEAD_RATE_WINDOW_SECONDS, MAX_RATE_LIMIT_CLIENTS
)

def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))


def close_db_resources(cur, conn) -> None:
    """Close both resources even if closing one fails."""
    if cur is not None:
        with suppress(Exception):
            cur.close()
    if conn is not None:
        with suppress(Exception):
            conn.close()


def init_db():
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                created_at TIMESTAMP DEFAULT NOW(),
                tour_title TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                mobile TEXT,
                tour_dates_preferred TEXT,
                quantity INTEGER DEFAULT 1,
                currency TEXT DEFAULT 'USD',
                amount NUMERIC(10,2),
                type TEXT DEFAULT 'SpiritualToursToIndia',
                source_url TEXT,
                message TEXT,
                notification_status TEXT NOT NULL DEFAULT 'pending',
                notification_attempts INTEGER NOT NULL DEFAULT 0,
                notification_attempted_at TIMESTAMP
            )
        """)
        cur.execute("ALTER TABLE leads ADD COLUMN IF NOT EXISTS message TEXT")
        cur.execute(
            "ALTER TABLE leads ADD COLUMN IF NOT EXISTS notification_status "
            "TEXT NOT NULL DEFAULT 'pending'"
        )
        cur.execute(
            "ALTER TABLE leads ADD COLUMN IF NOT EXISTS notification_attempts "
            "INTEGER NOT NULL DEFAULT 0"
        )
        cur.execute(
            "ALTER TABLE leads ADD COLUMN IF NOT EXISTS notification_attempted_at TIMESTAMP"
        )
        cur.execute("CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at)")
        conn.commit()
    finally:
        close_db_resources(cur, conn)

init_db()

class LeadCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    tour_title: str = Field(min_length=1, max_length=200)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: str = Field(
        min_length=3, max_length=254, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )
    mobile: Optional[str] = Field(default=None, max_length=40)
    tour_dates_preferred: Optional[str] = Field(default=None, max_length=200)
    quantity: int = Field(default=1, ge=1, le=100)
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    amount: Optional[float] = Field(default=None, ge=0, le=10_000_000)
    type: str = Field(default="SpiritualToursToIndia", min_length=1, max_length=100)
    source_url: Optional[str] = Field(default=None, max_length=2048)
    message: Optional[str] = Field(default=None, max_length=5000)
    # Deliberately hidden from legitimate forms; non-empty values are accepted
    # with a success response but are never persisted or forwarded.
    website: Optional[str] = Field(default=None, max_length=200)

class LeadResponse(BaseModel):
    success: bool
    message: str
    lead_id: Optional[str] = None
    notification_sent: Optional[bool] = None

def require_admin(authorization: Optional[str] = Header(default=None)) -> None:
    """Protect lead exports containing personal information."""
    expected = os.environ.get("SESSION_SECRET")
    supplied = authorization.removeprefix("Bearer ").strip() if authorization else ""
    if not expected or not supplied or not secrets.compare_digest(supplied, expected):
        raise HTTPException(status_code=401, detail="Valid admin bearer token required")


def lead_client_id(request: Request) -> str:
    """Prefer Cloudflare's client-IP header when the proxy supplies it."""
    cloudflare_ip = request.headers.get("CF-Connecting-IP")
    if cloudflare_ip:
        return cloudflare_ip.strip()
    return request.client.host if request.client else "unknown"


@app.post("/api/leads", response_model=LeadResponse)
async def create_lead(lead: LeadCreate, request: Request):
    if not lead_rate_limiter.allow(lead_client_id(request)):
        raise HTTPException(
            status_code=429,
            detail="Too many submissions. Please try again later.",
            headers={"Retry-After": str(LEAD_RATE_WINDOW_SECONDS)},
        )

    if lead.website:
        return LeadResponse(
            success=True,
            message="Enquiry submitted successfully! We'll get back to you soon.",
        )

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        lead_id = str(uuid.uuid4())
        cur.execute("""
            INSERT INTO leads (id, tour_title, first_name, last_name, email, mobile, 
                             tour_dates_preferred, quantity, currency, amount, type, source_url, message)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            lead_id,
            lead.tour_title,
            lead.first_name,
            lead.last_name,
            lead.email,
            lead.mobile,
            lead.tour_dates_preferred,
            lead.quantity,
            lead.currency,
            lead.amount,
            lead.type,
            lead.source_url,
            lead.message
        ))
        conn.commit()
    except Exception:
        if conn is not None:
            with suppress(Exception):
                conn.rollback()
        logger.exception("Lead storage failed")
        raise HTTPException(status_code=500, detail="Unable to submit enquiry") from None
    finally:
        close_db_resources(cur, conn)

    notification_sent = await send_notification_email(lead, lead_id)
    record_notification_result(lead_id, notification_sent)
    return LeadResponse(
        success=True,
        message=(
            "Enquiry submitted successfully! We'll get back to you soon."
            if notification_sent
            else "Your enquiry has been saved. Our team will follow up soon."
        ),
        lead_id=lead_id,
        notification_sent=notification_sent,
    )


def record_notification_result(lead_id: str, sent: bool) -> None:
    """Persist delivery state so failed notifications are visible to admins."""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE leads
            SET notification_status = %s,
                notification_attempts = notification_attempts + 1,
                notification_attempted_at = NOW()
            WHERE id = %s
            """,
            ("sent" if sent else "failed", lead_id),
        )
        conn.commit()
    except Exception:
        if conn is not None:
            with suppress(Exception):
                conn.rollback()
        logger.exception("Unable to persist notification status for lead %s", lead_id)
    finally:
        close_db_resources(cur, conn)


async def send_notification_email(lead: LeadCreate, lead_id: str) -> bool:
    try:
        email_body = f"""
New Tour Enquiry Received!

Lead ID: {lead_id}
Tour: {lead.tour_title}
Type: {lead.type}

Contact Details:
- Name: {lead.first_name} {lead.last_name}
- Email: {lead.email}
- Mobile: {lead.mobile or 'Not provided'}

Tour Preferences:
- Preferred Dates: {lead.tour_dates_preferred or 'Not specified'}
- Number of Travelers: {lead.quantity}
- Budget: {lead.currency} {lead.amount if lead.amount else 'Not specified'}
- Message: {lead.message or 'Not provided'}

Source: {lead.source_url or 'Direct'}

---
Spiritual Tours to India Lead Management System
        """
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                CLOUDFLARE_WORKER_URL,
                json={
                    "name": f"{lead.first_name} {lead.last_name}",
                    "email": lead.email,
                    "phone": lead.mobile or "",
                    "tour": lead.tour_title,
                    "dates": lead.tour_dates_preferred or "",
                    "message": email_body,
                    "recipients": EMAIL_RECIPIENTS
                },
                timeout=10.0
            )
            return 200 <= response.status_code < 300
    except Exception:
        logger.exception("Email notification failed")
        return False

@app.get("/api/leads")
async def get_leads(_: None = Depends(require_admin)):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, created_at, tour_title, first_name, last_name, email, mobile,
                   tour_dates_preferred, quantity, currency, amount, type, source_url, message,
                   notification_status, notification_attempts, notification_attempted_at
            FROM leads
            ORDER BY created_at DESC
            LIMIT 100
        """)
        leads = cur.fetchall()
        return {
            "success": True,
            "leads": [
                {
                    "id": str(row[0]),
                    "created_at": row[1].isoformat() if row[1] else None,
                    "tour_title": row[2],
                    "first_name": row[3],
                    "last_name": row[4],
                    "email": row[5],
                    "mobile": row[6],
                    "tour_dates_preferred": row[7],
                    "quantity": row[8],
                    "currency": row[9],
                    "amount": float(row[10]) if row[10] else None,
                    "type": row[11],
                    "source_url": row[12],
                    "message": row[13],
                    "notification_status": row[14],
                    "notification_attempts": row[15],
                    "notification_attempted_at": (
                        row[16].isoformat() if row[16] else None
                    )
                }
                for row in leads
            ]
        }
    except Exception:
        logger.exception("Lead retrieval failed")
        raise HTTPException(status_code=500, detail="Unable to retrieve leads") from None
    finally:
        close_db_resources(cur, conn)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
