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
*   **Email Service**: For contact (namaste@smukti.com).

### CSS & Font Dependencies

*   **Tailwind CSS**: Version 2.2.19, delivered via Cloudflare CDN.
*   **Google Fonts**: Lora (serif) and Inter (sans-serif), with preconnect optimization.

### Browser APIs

Native Web APIs are used, including Smooth Scroll API, DOM Manipulation APIs, and Event Listeners (click, scroll).