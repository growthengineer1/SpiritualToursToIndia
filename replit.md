# Spiritual Tours to India - Landing Page

## Overview

A high-converting, SEO-optimized static HTML landing page designed to help international travelers (primarily from USA, Canada, UK, Europe, and Australia) research and plan spiritual tours to India. The site serves as an informational resource that connects users with tour organizers through consultation bookings and contact forms.

**Primary Purpose**: Generate qualified leads for spiritual tour packages by providing curated itineraries, destination guides, and travel resources.

**Target Keywords**: spiritual tours to india, spiritual tour to india, spiritual travel india, spiritual journey to india, yoga tours india, meditation retreats india, temple tours india

## Recent Changes

### October 15, 2025 - Image Optimization & Path Fix for Production

- **CRITICAL CSS Bug Fix - Images Not Displaying**: Fixed CSS rule that was hiding ALL images on the site
  - **Problem**: `img[loading="lazy"] { opacity: 0; }` rule made all lazy-loaded images invisible
  - **Root Cause**: CSS expected JavaScript to add `.loaded` class, but no JS existed to do this
  - **Solution**: Removed the opacity: 0 rule from custom.css (lines 98-100)
  - **Impact**: All images now display correctly (hero, destinations, tours, testimonials, blog posts)
  - **Result**: Verified all images loading with 200 status codes in server logs
  - Images still lazy-load natively via browser (no fade-in animation, but functional)

- **Image Optimization - WebP Conversion**: Resolved mobile loading issues with oversized images
  - Converted 7 blog images from PNG to WebP format
  - File size reduction: 712KB-2.0MB → 23KB-138KB (90-95% smaller)
  - Images now load instantly on mobile devices and slow connections
  - All modern browsers support WebP (Chrome, Safari, Firefox, Edge)

- **Critical Fix - Absolute Image Paths**: Resolved blog images not displaying on production site
  - Changed all image paths from relative (`attached_assets/...`) to absolute (`/attached_assets/...`)
  - Fixed 25 image references: 18 stock images (testimonials + blogs 1-3) + 7 blog images (blogs 4-10)
  - Absolute paths ensure consistent loading across all pages and deployment environments
  - Images work in development (Python server) and production (Cloudflare Pages)
  
- **Blog Images Permissions Fix**: Resolved accessibility issue with blog images in Python HTTP server
  - Set directory permissions to 755 on `attached_assets/blog_images/`
  - All 7 blog images now accessible and loading correctly
  - Verified via server logs (200 status codes)
  
- **Image Hosting Architecture Clarification**: 
  - Confirmed Replit App Storage blueprint is incompatible with static HTML sites (requires Node.js/TypeScript backend)
  - Current working setup uses local storage + external CDN approach:
    - 18 stock images in `attached_assets/stock_images/` (testimonials, blog posts 1-3)
    - 7 blog images in `attached_assets/blog_images/` (blog posts 4-10)
    - 12 destination/tour images from Unsplash CDN (external)
  - All images verified working with proper permissions

### October 14, 2025 - Analytics & Asset Optimization
- **Google Tag Manager Installation**: Implemented GTM container (GTM-T65DHKXL) across entire site for analytics and conversion tracking
  - Head script installed immediately after `<head>` tag on all pages
  - Noscript iframe installed immediately after `<body>` tag on all pages
  - Deployed on: index.html + all 6 tour detail pages (golden-triangle, south-india, karnataka, char-dham, buddha-circuit, tamil-nadu-kerala)
  
- **Blog Image Migration**: Migrated 7 blog featured images from external Bubble CDN to local hosting
  - Downloaded images from smukti.com/bubble.io CDN to `attached_assets/blog_images/`
  - Updated HTML references from external URLs to local paths
  - Resolved CORS/security policy blocking issues with external CDN images
  - Affected images: transportation.png, packing.png, health.png, sacred-architecture.png, visa.png, first-time.png, women-safety.png

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Static Site Approach**
- Pure HTML5/CSS/JavaScript with no build tools or frameworks
- Mobile-first responsive design using Tailwind CSS utility classes
- Semantic HTML5 markup for SEO optimization
- Custom CSS extends Tailwind for specific design requirements

**Rationale**: Static HTML provides maximum performance, simplicity, and SEO benefits for a landing page. No backend processing needed since this is purely informational with external service integrations for forms and bookings.

### Content Structure

**12-Section Landing Page Layout**
1. Sticky header navigation
2. Hero section with primary CTA
3. Value proposition (Why India)
4. Destination showcase
5. Curated tour itineraries
6. Spiritual experience types
7. Social proof (testimonials)
8. Travel resources/blog preview
9. FAQ accordion
10. Consultation CTA
11. Contact form
12. Footer

**Design Pattern**: Long-form landing page optimized for conversion, with progressive disclosure of information and multiple conversion points throughout the scroll journey.

### Styling Approach

**Tailwind CSS via CDN**
- Utility-first CSS framework loaded from Cloudflare CDN
- No build process required
- Custom CSS file (`assets/css/custom.css`) for extended styles beyond Tailwind utilities

**Typography Stack**:
- Headings: 'Lora' (serif, elegant for spiritual theme)
- Body: 'Inter' (sans-serif, optimized for readability)
- Loaded via Google Fonts

**Rationale**: CDN approach eliminates build complexity while providing full Tailwind functionality. Custom fonts enhance brand personality appropriate for spiritual/cultural content.

### Interactive Features

**Vanilla JavaScript Implementation**
- Mobile hamburger menu toggle
- FAQ accordion with smooth animations
- Smooth scroll with header offset compensation
- No framework dependencies

**Animation Strategy**: CSS transitions for performance, JavaScript only for state management. Scroll-reveal animations use CSS transforms for GPU acceleration.

### SEO Architecture

**On-Page Optimization**
- Semantic HTML5 structure with proper heading hierarchy
- Comprehensive meta tags (description, keywords, Open Graph, Twitter Cards)
- Schema.org structured data (TravelAgency type)
- Canonical URL specification
- Strategic internal anchor linking with scroll offset

**Rationale**: Static HTML enables perfect SEO control. Schema markup helps search engines understand the business type and improves rich snippet potential.

### Asset Management

**Image Strategy**
- Primary images hosted on Supabase storage
- Optimized for web delivery
- Responsive image considerations for mobile

**Rationale**: Supabase provides reliable CDN-backed storage without managing separate image infrastructure. Keeps repository lightweight.

## External Dependencies

### Hosting & Deployment

**Cloudflare Pages**
- Git-based continuous deployment
- Automatic deployment triggered by GitHub pushes
- Global CDN distribution
- SSL/TLS included

**GitHub Repository**
- Source code version control
- Triggers Cloudflare Pages deployments

**Rationale**: Cloudflare Pages offers zero-config deployment with excellent performance for static sites. GitHub integration enables version control and automated deployment workflows.

### Domain & DNS

**Cloudflare DNS**
- Domain: spiritualtourstoindia.com
- DNS management through Cloudflare

### Third-Party Service Integrations

**Calendly**
- Consultation booking system
- Link: https://calendly.com/sabin-smukti/30min
- Opens in new tab for 30-minute consultation scheduling

**WhatsApp Business**
- Quick messaging option for user inquiries
- Phone: +918807070819
- Direct mobile communication channel

**Supabase**
- Image storage and delivery
- No database or backend API usage
- CDN-backed asset hosting only

**Email Service**
- Contact email: namaste@smukti.com
- Form submissions likely handled client-side or via external form service

### CSS & Font Dependencies

**Tailwind CSS**
- Version: 2.2.19
- Delivery: Cloudflare CDN
- URL: https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css

**Google Fonts**
- Lora (serif): weights 400, 600, 700
- Inter (sans-serif): weights 300, 400, 500, 600
- Preconnect optimization for performance

**Rationale**: CDN delivery eliminates build tools while maintaining fast load times. Font preconnect reduces latency for typography loading.

### Browser APIs

**Native Web APIs Used**
- Smooth Scroll API
- DOM Manipulation APIs
- Event Listeners (click, scroll)
- LocalStorage (potential for form data persistence)