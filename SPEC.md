# GEOPRAM TECHNOLOGIES - Website Specification

## 1. Project Overview

**Project Name:** GEOPRAM TECHNOLOGIES Website  
**Project Type:** Django-based Multi-page Professional Website with Dashboard  
**Core Functionality:** A comprehensive GIS services company website showcasing mapping, remote sensing, AI analysis, web development, design services, training programs, and a professional client dashboard.  
**Target Users:** Surveyors, GIS professionals, businesses needing spatial solutions, students seeking GIS training

---

## 2. UI/UX Specification

### Layout Structure

**Pages:**
1. **Home** - Hero, services overview, features, testimonials, CTA
2. **Services** - Detailed GIS services (Mapping, Remote Sensing, AI Analysis, Web Dev, Design)
3. **Software/Apps** - Compatible tools (RTK, AutoCAD, GIS software showcase)
4. **Solutions** - Industry-specific solutions
5. **Training** - Courses (Django, GIS, etc.)
6. **Dashboard** - Professional client portal (login required)
7. **Contact** - Contact form and info

**Responsive Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Visual Design

**Color Palette:**
- Primary: `#0A2540` (Deep navy blue)
- Secondary: `#00D4AA` (Teal/Cyan accent)
- Accent: `#FF6B35` (Orange for CTAs)
- Background: `#0D1117` (Dark mode base)
- Surface: `#161B22` (Card backgrounds)
- Text Primary: `#E6EDF3`
- Text Secondary: `#8B949E`
- Success: `#3FB950`
- Warning: `#D29922`

**Typography:**
- Headings: "Outfit" (Google Fonts) - Bold, modern geometric sans
- Body: "DM Sans" (Google Fonts) - Clean, readable
- Monospace/Code: "JetBrains Mono"
- H1: 56px, H2: 40px, H3: 28px, H4: 22px
- Body: 16px, Small: 14px

**Spacing System:**
- Base unit: 8px
- Section padding: 80px vertical
- Card padding: 24px
- Gap: 16px, 24px, 32px

**Visual Effects:**
- Glassmorphism cards with `backdrop-filter: blur(12px)`
- Gradient borders using pseudo-elements
- Subtle glow effects on hover
- Smooth scroll behavior
- Entrance animations with stagger

### Components

**Navigation:**
- Fixed top navbar with blur background
- Logo on left, nav links center, CTA button right
- Mobile: hamburger menu with slide-in drawer

**Hero Section:**
- Full viewport height
- Animated gradient background with floating geometric shapes
- Main headline with typewriter or fade-in effect
- Subheadline and dual CTA buttons

**Service Cards:**
- Icon + title + description
- Hover: lift effect with glow border
- 3-column grid on desktop, 1-column mobile

**Stats Counter:**
- Animated number counting
- Icon + number + label
- Glassmorphism background

**Testimonials:**
- Carousel/slider
- Avatar, name, company, quote
- Navigation dots

**Dashboard:**
- Sidebar navigation (collapsible)
- Top bar with user info
- Main content area with cards/widgets
- Charts for analytics (using Chart.js)

**Footer:**
- 4-column layout: About, Services, Quick Links, Contact
- Social icons
- Copyright

---

## 3. Functionality Specification

### Core Features

1. **Home Page**
   - Animated hero with company intro
   - Services preview (6 cards)
   - Stats section (projects, clients, years, training)
   - Featured software/tools showcase
   - Testimonials carousel
   - Contact CTA section

2. **Services Page**
   - Service categories with detailed descriptions
   - Mapping services
   - Remote sensing
   - AI/ML analysis for spatial data
   - Web development (GIS web apps)
   - Design services (posters, banners, maps visualization)

3. **Software/Apps Page**
   - RTK equipment support showcase
   - AutoCAD integration
   - GIS Software (QGIS, ArcGIS, etc.)
   - GIS Apps gallery
   - Compatibility badges

4. **Solutions Page**
   - Industry solutions (Surveying, Agriculture, Urban Planning, Mining, Environmental)
   - Case studies preview
   - Custom solutions form

5. **Training Page**
   - Django development courses
   - GIS certification courses
   - Computer skills training
   - Course cards with enrollment CTA
   - Schedule/calendar view

6. **Dashboard (Authenticated)**
   - Overview statistics widgets
   - Recent projects
   - Training progress
   - Messages/notifications
   - File downloads
   - Profile settings

7. **Contact Page**
   - Contact form (name, email, phone, message)
   - Company info (address, phone, email, social)
   - Embedded map placeholder

### User Interactions

- Smooth scroll navigation
- Form validation with inline errors
- Loading states on form submission
- Toast notifications for actions
- Mobile menu toggle
- Dashboard sidebar toggle
- Carousel navigation

### Data Handling

- Django templates for static content
- Django forms for contact/training enrollment
- Session-based authentication for dashboard
- Static files (CSS, JS, images)

---

## 4. Acceptance Criteria

1. ✅ All pages render without errors
2. ✅ Navigation works between all pages
3. ✅ Responsive on mobile, tablet, desktop
4. ✅ Dashboard login/logout functional
5. ✅ Contact form validates and shows success message
6. ✅ Animations play smoothly
7. ✅ Color scheme matches spec exactly
8. ✅ Typography loads correctly
9. ✅ All interactive elements have hover states
10. ✅ Professional appearance suitable for B2B GIS company