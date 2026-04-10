# User Acceptance Testing (UAT) - Mechanical Insight

## Test Environment
- Browser: Chrome 120+, Firefox 115+, Safari 17+
- Devices: Desktop (1920x1080), Tablet (768x1024), Mobile (375x812)
- URL: https://mechanical-insight.onrender.com

## UAT Test Cases

### TC-001: Homepage Navigation
- **Scenario:** User visits the homepage
- **Steps:** Navigate to / → Verify hero section loads → Check services overview → Verify statistics counter animates → Check CTA buttons work
- **Expected:** All sections render correctly, animations play, links navigate properly
- **Status:** PASSED

### TC-002: Services Browsing
- **Scenario:** User browses engineering services
- **Steps:** Click "Services" in navbar → Verify all 7 services displayed → Click on a service → Verify detail page loads with description
- **Expected:** Grid layout shows all services, detail page shows full info with related case studies
- **Status:** PASSED

### TC-003: Contact Form Submission
- **Scenario:** User submits contact inquiry
- **Steps:** Navigate to /contact → Fill all required fields → Submit form → Verify success message
- **Expected:** Form validates inputs, saves to database, shows success feedback
- **Status:** PASSED

### TC-004: Contact Form Validation
- **Scenario:** User submits invalid form data
- **Steps:** Submit empty form → Submit with invalid email → Submit with short message
- **Expected:** Appropriate validation errors shown for each field
- **Status:** PASSED

### TC-005: Blog Browsing
- **Scenario:** User reads blog posts
- **Steps:** Navigate to /blog → Browse posts → Click on a post → Verify full content loads
- **Expected:** Blog listing with pagination, post detail with related posts
- **Status:** PASSED

### TC-006: Blog Search & Categories
- **Scenario:** User searches and filters blog posts
- **Steps:** Use search bar → Search for "CFD" → Click category filter
- **Expected:** Relevant results displayed, category filtering works
- **Status:** PASSED

### TC-007: Portfolio Browsing
- **Scenario:** User views case studies
- **Steps:** Navigate to /portfolio → Browse case studies → Click on one → Verify challenge/solution/results
- **Expected:** Grid layout, detail page with full case study structure
- **Status:** PASSED

### TC-008: Newsletter Subscription
- **Scenario:** User subscribes to newsletter
- **Steps:** Enter email in footer form → Click subscribe → Verify confirmation
- **Expected:** Success message, email saved, duplicate prevention works
- **Status:** PASSED

### TC-009: Admin Login
- **Scenario:** Admin logs into dashboard
- **Steps:** Navigate to /admin/login → Enter credentials → Verify dashboard loads
- **Expected:** Successful login, dashboard shows statistics
- **Status:** PASSED

### TC-010: Admin Dashboard
- **Scenario:** Admin manages content
- **Steps:** View dashboard stats → Check contact submissions → View subscribers
- **Expected:** All admin sections accessible, data displays correctly
- **Status:** PASSED

### TC-011: Mobile Responsiveness
- **Scenario:** User accesses site on mobile device
- **Steps:** Resize browser to mobile → Check navbar hamburger menu → Navigate all pages
- **Expected:** All pages render correctly, touch-friendly navigation
- **Status:** PASSED

### TC-012: Cross-Browser Testing
- **Scenario:** Site works across browsers
- **Steps:** Test in Chrome → Test in Firefox → Test in Safari → Test in Edge
- **Expected:** Consistent rendering and functionality across all browsers
- **Status:** PASSED

### TC-013: Global Search
- **Scenario:** User searches across all content
- **Steps:** Use navbar search → Search for engineering term → Verify results from blog, portfolio, services
- **Expected:** Results categorized by content type, relevant matches highlighted
- **Status:** PASSED

### TC-014: Error Handling
- **Scenario:** User encounters errors
- **Steps:** Navigate to invalid URL → Verify 404 page → Test server error handling
- **Expected:** Custom error pages displayed with navigation back to homepage
- **Status:** PASSED

### TC-015: Image Loading
- **Scenario:** Portfolio images load correctly
- **Steps:** Browse portfolio → Verify all images load → Check image optimization
- **Expected:** All images load without broken links, optimized file sizes
- **Status:** PASSED

## UAT Summary
- **Total Test Cases:** 15
- **Passed:** 15
- **Failed:** 0
- **Completion Rate:** 100%
- **UAT Sign-off:** Approved by Product Owner
- **Date:** April 10, 2026
