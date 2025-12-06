import os
import uuid
from datetime import datetime
from typing import Optional

import httpx
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Spiritual Tours to India API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLOUDFLARE_WORKER_URL = "https://spiritualtourstoindiaemail.sabin.workers.dev"
EMAIL_RECIPIENTS = ["namaste@smukti.com", "sabin@smukti.com"]

def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

def init_db():
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
            source_url TEXT
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at)")
    conn.commit()
    cur.close()
    conn.close()

init_db()

class LeadCreate(BaseModel):
    tour_title: str
    first_name: str
    last_name: str
    email: str
    mobile: Optional[str] = None
    tour_dates_preferred: Optional[str] = None
    quantity: Optional[int] = 1
    currency: Optional[str] = "USD"
    amount: Optional[float] = None
    type: Optional[str] = "SpiritualToursToIndia"
    source_url: Optional[str] = None

class LeadResponse(BaseModel):
    success: bool
    message: str
    lead_id: Optional[str] = None

@app.post("/api/leads", response_model=LeadResponse)
async def create_lead(lead: LeadCreate):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        lead_id = str(uuid.uuid4())
        
        cur.execute("""
            INSERT INTO leads (id, tour_title, first_name, last_name, email, mobile, 
                             tour_dates_preferred, quantity, currency, amount, type, source_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            lead.source_url
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        email_sent = await send_notification_email(lead, lead_id)
        
        return LeadResponse(
            success=True,
            message="Enquiry submitted successfully! We'll get back to you soon.",
            lead_id=lead_id
        )
        
    except Exception as e:
        print(f"Error creating lead: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
            return response.status_code == 200
    except Exception as e:
        print(f"Email notification failed: {e}")
        return False

@app.get("/api/leads")
async def get_leads():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, created_at, tour_title, first_name, last_name, email, mobile,
                   tour_dates_preferred, quantity, currency, amount, type, source_url
            FROM leads
            ORDER BY created_at DESC
            LIMIT 100
        """)
        leads = cur.fetchall()
        cur.close()
        conn.close()
        
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
                    "source_url": row[12]
                }
                for row in leads
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/attached_assets", StaticFiles(directory="attached_assets"), name="attached_assets")
app.mount("/destinations", StaticFiles(directory="destinations", html=True), name="destinations")

@app.get("/")
async def serve_index():
    return FileResponse("index.html")

@app.get("/{path:path}")
async def serve_static(path: str):
    if os.path.exists(path):
        return FileResponse(path)
    if os.path.exists(f"{path}.html"):
        return FileResponse(f"{path}.html")
    return FileResponse("index.html")
