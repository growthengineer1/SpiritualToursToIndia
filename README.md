# Spiritual Tours to India - Landing Page

A high-converting, SEO-optimized static HTML landing page for spiritualtourstoindia.com - a planning resource for international travelers researching spiritual tours to India.

## Project Overview

This landing page helps users plan their spiritual journey and connects them with tour organizers. It features curated tour itineraries, destination guides, travel resources, and booking options.

## Tech Stack

- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first CSS framework (via CDN)
- **JavaScript** - Interactive features
- **Deployment**: Cloudflare Pages (auto-deploy from GitHub)
- **Images**: Supabase storage

## Features

- Fully responsive design (mobile-first approach)
- SEO-optimized with meta tags and schema markup
- Interactive FAQ accordion
- Contact form with Cloudflare Worker + SendGrid email delivery
- Mobile navigation menu
- Smooth scrolling
- WhatsApp and Calendly integration

## Sections

1. Header/Navigation (sticky)
2. Hero Section
3. Why India for Spiritual Journey
4. Popular Spiritual Destinations
5. Curated Tour Itineraries
6. Types of Spiritual Experiences
7. Traveler Testimonials
8. Essential Travel Resources (Blog)
9. FAQ
10. Consultation CTA
11. Contact Form
12. Footer

## Local Development

Simply open `index.html` in a browser or use a local server:

```bash
python -m http.server 5000
# or
npx serve
```

## Deployment

Deployed via Cloudflare Pages with auto-deployment from GitHub main branch.

## Email Integration

Contact form uses a **Cloudflare Worker** with **SendGrid REST API** for email delivery:

- **Worker Endpoint**: `spiritualtourstoindiaemail.sabin.workers.dev`
- **Email From**: `namaste@smukti.com`
- **Email To**: `hello@spiritualtourstoindia.com`
- **API**: SendGrid (API key stored as Cloudflare environment variable)

**To deploy the Worker:**
1. Copy code from `worker.js` 
2. Paste into Cloudflare Workers dashboard or deploy via Wrangler CLI
3. Ensure `SENDGRID_API_KEY` environment variable is set in Cloudflare

## Contact

- Email: hello@spiritualtourstoindia.com
- WhatsApp: +918807070819
- Booking: https://calendly.com/sabin-smukti/30min

## License

All rights reserved © 2025 Spiritual Tours to India
