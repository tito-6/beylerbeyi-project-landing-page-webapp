# Overview

This is a luxury real estate landing page for "Beylerbeyi Bosphorus Residences" in Istanbul, Turkey. The application is designed to capture high-quality leads for a premium residential development project with Bosphorus views. It focuses on conversion optimization through elegant design, multi-language support, and comprehensive lead tracking capabilities.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Flask-based Web Application**: Uses Flask as the web framework with Jinja2 templating for server-side rendering
- **Responsive Design**: Bootstrap 5 framework provides mobile-first responsive layout with custom CSS for luxury aesthetics
- **Multi-language Support**: Static JSON-based internationalization supporting Turkish (default), English, and Arabic with RTL layout support
- **Premium UI/UX**: Black/white/gold color scheme with Playfair Display serif font for headlines and Inter for body text, designed for luxury real estate market

## Backend Architecture
- **Flask Application Structure**: Modular design with separate files for routes, models, utilities, and configuration
- **SQLAlchemy ORM**: Database abstraction layer using DeclarativeBase pattern for model definitions
- **Lead Management**: Comprehensive lead capture system with detailed form data including UTM tracking parameters
- **Email Integration**: Flask-Mail for automated email notifications to sales team and auto-reply functionality
- **Session Management**: Flask sessions for language preference persistence

## Data Storage Solutions
- **Primary Database**: Configurable via DATABASE_URL environment variable (defaults to SQLite for development)
- **Lead Model**: Comprehensive lead tracking including contact information, preferences, consent management, UTM parameters, and technical metadata (IP, user agent)
- **KVKK Compliance**: Built-in support for Turkish GDPR compliance with consent tracking

## External Dependencies
- **Email Services**: SMTP integration (configured for Gmail by default) for lead notifications and auto-replies
- **Analytics Integration**: Multi-platform tracking setup including Google Analytics 4, Google Tag Manager, Meta Pixel, and LinkedIn Insight Tag
- **WhatsApp Integration**: Direct WhatsApp links with pre-filled messages for instant communication
- **Font Services**: Google Fonts integration for premium typography (Playfair Display, Inter)
- **CDN Resources**: Bootstrap 5 and Font Awesome via CDN for UI components and icons
- **Maps Integration**: Google Maps iframe for location display (mentioned in documentation)

The architecture prioritizes lead conversion, performance optimization, and compliance while maintaining a luxury brand experience across multiple languages and devices.