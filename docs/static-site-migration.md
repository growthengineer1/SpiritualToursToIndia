# Static-site/API migration

## Target architecture

Cloudflare Pages serves this repository's static files from the repository root. FastAPI is API-only and continues to expose:

- `POST /api/leads` — public lead submission
- `GET /api/leads` — lead administration endpoint; send `Authorization: Bearer`
  using `SESSION_SECRET` (never expose its value in client code or documentation)
- `GET /api/health` — health check

There is intentionally no FastAPI fallback, static-file mount, or HTML route.
The production form base URL is intended to be
`https://api.spiritualtourstoindia.com`; its DNS and API deployment still need
to be completed, so production forms will not work until that cutover is done.

Credentialed API CORS is limited to `https://spiritualtourstoindia.com` and `https://www.spiritualtourstoindia.com`. The only development origins enabled are the documented loopback servers:

- `http://localhost:3000`, `http://localhost:5000`, `http://localhost:5173`
- `http://127.0.0.1:3000`, `http://127.0.0.1:5000`, `http://127.0.0.1:5173`

Add a new origin only by code review; do not use wildcard CORS with credentials.

## Lead submission abuse protection

The API applies a small per-process submission limit as an application-layer
defense. Cloudflare edge rate limiting and bot protection remain required in
production: in-memory limits are not shared across API processes and reset on
process restart.

## URL map

This map is derived from the current `sitemap.xml`. Every listed path is an exact static file path on Pages unless noted otherwise. The `.html` suffixes must remain in deployment output.

| URL paths | Action |
| --- | --- |
| `/` | Serve `index.html` |
| `/essential-trip-info.html`, `/privacy-policy.html`, `/terms.html` | Serve unchanged |
| `/tours/varanasi-spirituality.html`, `/tours/rishikesh-yoga.html`, `/tours/delhi-uttarakhand.html`, `/tours/goa-wellness.html`, `/tours/kerala-ayurveda.html`, `/tours/himalayan-trek.html` | Serve unchanged |
| `/tours/women-rising.html`, `/tours/love-alchemy.html`, `/tours/grieving-grace.html`, `/tours/chakra-awakening.html` | Serve unchanged |
| `/tours/sound-healing.html`, `/tours/sacred-feminine-cycle.html`, `/tours/creative-awakening.html`, `/tours/ancestral-healing.html` | Serve unchanged |
| `/tours/sacred-geometry.html`, `/tours/festival-tours.html`, `/tours/silver-years.html` | Serve unchanged |
| `/tours/golden-triangle.html`, `/tours/south-india.html`, `/tours/buddha-circuit.html`, `/tours/char-dham.html`, `/tours/karnataka.html`, `/tours/tamil-nadu-kerala.html` | Serve unchanged |
| `/destinations/varanasi.html`, `/destinations/rishikesh.html`, `/destinations/bodh-gaya.html`, `/destinations/haridwar.html`, `/destinations/south-india.html`, `/destinations/himalayan-sanctuaries.html`, `/destinations/hampi.html`, `/destinations/tiruvannamalai.html`, `/destinations/kanyakumari.html` | Serve unchanged |
| `/tours/golden-triangle-spiritual.html` | **301** redirect to `/tours/golden-triangle.html` via `_redirects` |
| `/robots.txt`, `/sitemap.xml` | Serve unchanged |

`/tours/golden-triangle-spiritual.html` is retained as an inbound URL through a
single permanent redirect, rather than a duplicate page. It is not included in
the sitemap; only the destination URL is indexed there.

## Cutover and rollback

1. Deploy the repository root to a Cloudflare Pages preview. Confirm every URL above returns `200`, except the Golden Triangle spiritual URL, which returns one `301` followed by `200`.
2. Confirm `/robots.txt` and `/sitemap.xml` are served from Pages, then test a real `POST /api/leads` from each production hostname and check `/api/health` at the API origin.
3. Point the production hostname to the verified Pages deployment. Monitor HTTP status coverage, redirect chains, form submissions, and Search Console for 10–14 days before subsequent content releases.
4. To roll back, restore the preceding known-good Cloudflare Pages deployment (or DNS origin), retain the API deployment and database, and re-check the URL map and lead submission. Do not replace the 301 with a temporary redirect during rollback.

## Search Console publication gates

- **Before each wave:** verify the canonical URL list, one-hop redirects,
  production `200` coverage, sitemap submission, and a real lead submission
  after the API hostname is live.
- **Observation gate (10–14 days):** proceed only if Search Console shows no
  material rise in excluded, duplicate, soft-404, or server-error URLs and
  indexed pages retain expected impressions/clicks.
- **Stop/rollback gate:** pause the next wave and restore the prior Pages
  deployment if coverage errors persist, canonical selection is unexpected, or
  production lead capture fails. Record the affected URLs before retrying.