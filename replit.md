# Spiritual Tours to India - Landing Page

## Overview

A high-converting, SEO-optimized static HTML landing page designed to help international travelers (primarily from USA, Canada, UK, Europe, and Australia) research and plan spiritual tours to India. The site serves as an informational resource that connects users with tour organizers through consultation bookings and contact forms. The primary purpose is to generate qualified leads for spiritual tour packages by providing curated itineraries, destination guides, and travel resources.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

The project uses a static site approach with pure HTML5/CSS/JavaScript, no build tools or frameworks, and a mobile-first responsive design using Tailwind CSS utility classes. Semantic HTML5 markup is used for SEO optimization, and custom CSS extends Tailwind for specific design requirements. The content is structured as a 12-section landing page, optimized for conversion with progressive disclosure of information and multiple conversion points.

### Styling Approach

Tailwind CSS is loaded via CDN, eliminating the need for a build process. Custom CSS is used for extended styles. Typography uses 'Lora' (serif) for headings and 'Inter' (sans-serif) for body text, loaded via Google Fonts.

### Interactive Features

Interactive features are implemented with vanilla JavaScript for mobile menu toggles, FAQ accordions, and smooth scrolling. CSS transitions are used for performance, with JavaScript managing state.

### SEO Architecture

On-page optimization includes semantic HTML5 with proper heading hierarchy, comprehensive meta tags (description, keywords, Open Graph, Twitter Cards), Schema.org structured data (TravelAgency type), canonical URL specification, and strategic internal anchor linking.

### Asset Management

Images are hosted on Supabase storage, optimized for web delivery, and consider responsive design for mobile.

## External Dependencies

### Hosting & Deployment

**Cloudflare Pages** is used for Git-based continuous deployment, triggered by GitHub pushes, with global CDN distribution and SSL/TLS.
**GitHub Repository** provides source code version control.

### Domain & DNS

**Cloudflare DNS** manages the domain: spiritualtourstoindia.com.

### Third-Party Service Integrations

*   **Calendly**: For consultation bookings (https://calendly.com/sabin-smukti/30min).
*   **WhatsApp Business**: For quick messaging (+918807070819).
*   **Supabase**: Used solely for image storage and delivery (CDN-backed asset hosting).
*   **Email Service**: Cloudflare Worker + SendGrid REST API
    - Worker endpoint: spiritualtourstoindiaemail.sabin.workers.dev
    - Sends from: namaste@smukti.com
    - Delivers to: hello@spiritualtourstoindia.com
    - API key stored as Cloudflare environment variable (SENDGRID_API_KEY)

### CSS & Font Dependencies

*   **Tailwind CSS**: Version 2.2.19, delivered via Cloudflare CDN.
*   **Google Fonts**: Lora (serif) and Inter (sans-serif), with preconnect optimization.

### Browser APIs

Native Web APIs are used, including Smooth Scroll API, DOM Manipulation APIs, and Event Listeners (click, scroll).

## Recent Changes

### October 15, 2025 - Image Optimizations & Updates

- **Himalayan Sanctuaries Image Updated**: Replaced with stunning Kedarnath temple photo
  - Previous: Generic Unsplash Himalayan landscape
  - New: Kedarnath temple with snow-capped Himalayan peaks and marigold garlands
  - Massive optimization: 1.9MB PNG → 218KB WebP (88.8% reduction!)
  - Shows authentic Himalayan pilgrimage site with dramatic mountain backdrop
  - Image path: `/attached_assets/kedarnath_himalayan.webp`

- **Varanasi Destination Image Updated**: Replaced with new authentic photo of Varanasi ghats
  - Previous: Generic stock photo
  - New: Authentic Varanasi ghats and temples image
  - Converted to WebP format for optimization (385KB JPEG → 241KB WebP, 37% reduction)
  - Added object-center positioning for better cropping at 256px height
  - Image path: `/attached_assets/varanasi_new.webp`

- **Hero Banner Image Replaced**: New authentic group photo showing international travelers at South Indian temple
  - Previous: Indian flag/Varanasi ghats generic image
  - New: Real photo of foreigners in traditional white clothes with orange garlands at temple ceremony
  - Better represents target audience (international spiritual travelers)
  - Shows authentic spiritual experience visitors can expect
  - Image path: `/attached_assets/Foreigners in South INdia Temple_1760509121835.png`

- **Featured Group Tour Section Added**: "Discovering Shiva" prominently displayed in Tour Options
  - Featured badge with star icon to highlight special group tour
  - Large featured card layout with Nataraja image
  - Tour highlights: 10-day experience, Chidambaram/Thanjavur/Tiruvannamalai temples, cosmic dance ceremonies
  - Fixed departure dates displayed: Nov 7-16 2025, Dec 5-14 2025, Jan 21-30 2026, Feb 6-15 2026
  - Two CTAs: "Book This Tour" (primary orange) and "Learn More" (secondary outline)
  - Links to: https://smukti.com/spiritual-tours/discovering-shiva
  - Trust indicator: "Limited spots • Small group (max 12 travelers)"
  - Responsive design with image on left, content on right

- **XML Sitemap Created**: Full sitemap.xml for Google Search Console submission
  - Includes homepage and all 6 tour detail pages
  - Properly formatted with absolute URLs, lastmod dates, changefreq, priority
  - Accessible at: https://spiritualtourstoindia.com/sitemap.xml
  - robots.txt created with sitemap reference
  - Ready for Google Search Console submission

- **Button Hover Fix**: Fixed "Explore Tour Options" button text visibility
  - Added missing `.hover\:text-orange-600:hover` CSS class
  - Text now properly displays in orange on white background when hovered
  - Fixed in: assets/css/custom.css

- **SEO Enhancement - OG Image Created**: Professional Open Graph image for social sharing
  - Created 1200×630px OG image from hero temple photo (international travelers)
  - Optimized to 214KB JPEG (under 500KB SEO best practice)
  - Added complete OG meta tags: image width, height, alt text, site name
  - Added Twitter Card image and alt text tags
  - Added robots meta tag (index, follow)
  - Image path: `/assets/og-image.jpg`
  - Improves social sharing appearance on Facebook, LinkedIn, Twitter, WhatsApp

- **Email Migration**: Updated primary contact email across all assets
  - Changed from: namaste@smukti.com
  - Changed to: hello@spiritualtourstoindia.com
  - Updated in: index.html (Schema markup, form action, mailto links), README.md, replit.md
  - FormSubmit.co contact form now sends to new email address

- **Destination Pages Created**: Added 9 comprehensive destination detail pages
  - Created /destinations/ directory with full detail pages for all locations
  - Pages: Varanasi, Rishikesh, Bodh Gaya, Haridwar, South India, Himalayan Sanctuaries, Hampi, Tiruvannamalai, Kanyakumari
  - Each page includes: SEO meta tags, hero section, overview, attractions, experiences, best time to visit, related tours, CTAs
  - Made all 9 destination cards on homepage fully clickable with hover effects (image zoom, title color change)
  - Added 3 new destinations: Hampi (UNESCO ruins, 337KB→163KB WebP), Tiruvannamalai (Arunachala Hill, JPEG→24KB WebP), Kanyakumari (southernmost tip)
  - Updated sitemap.xml with all 9 destination pages (priority 0.7)
  - All pages feature authentic spiritual content for international travelers with internal linking to related tours

### October 15, 2025 - Cloudflare Worker Email Integration

- **Contact Form Migration**: Replaced FormSubmit.co with Cloudflare Worker + SendGrid
  - Created `worker.js` with SendGrid REST API integration
  - Worker endpoint: spiritualtourstoindiaemail.sabin.workers.dev
  - Sends formatted HTML emails from namaste@smukti.com to hello@spiritualtourstoindia.com
  - API key stored securely as Cloudflare environment variable
  - Updated contact form in index.html to POST to Worker endpoint
  - Enhanced JavaScript to handle JSON responses from Worker
  - Added CORS support for cross-origin requests
  - Improved error handling with specific error messages
  - Professional email template with branded styling