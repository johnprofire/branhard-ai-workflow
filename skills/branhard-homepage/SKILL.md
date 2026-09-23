# BRANHARD Homepage Design Skill

## Purpose

Design, rebuild, and improve the BRANHARD website homepage in code.

The goal is a premium editorial fashion ecommerce experience inspired by the visual references supplied for BRANHARD.

Reference site:
https://branhard-mwtsv25.public.builtwithrocket.new/

Do not copy another company's branding, logo, text, images, or proprietary implementation.

Use the references for general design direction:
- premium fashion presentation
- cinematic hero sections
- editorial layouts
- strong typography
- generous whitespace
- high-quality product photography
- simple navigation
- clear shopping paths

---

## BRANHARD Design Direction

The homepage should feel:

- Premium
- Modern
- Editorial
- Minimal
- Bold
- Streetwear-focused
- Fashion-first
- Mobile-first

Avoid:

- Generic ecommerce templates
- Excessive gradients
- Clutter
- Too many UI elements
- Excessive animations
- Unnecessary borders
- Random decorative text
- Copying another brand's identity

---

# HOMEPAGE STRUCTURE

## 1. Announcement Bar

Create a thin announcement bar at the top.

Possible content:

- New collection announcements
- Delivery information
- Limited drops
- Important store information

Keep it visually minimal.

---

## 2. Navigation

Desktop navigation should include:

- BRANHARD logo/wordmark
- Shop
- Collections
- New Arrivals
- About
- Search
- Account
- Cart

Mobile navigation:

- Menu
- BRANHARD logo
- Search
- Cart

Navigation must remain readable over hero imagery.

---

## 3. Hero Section

The hero is the most important visual section.

Use:

- Full-width campaign image or video
- Responsive media
- Image fallback
- Strong typography
- Short campaign statement
- Primary CTA
- Optional secondary CTA

BRANHARD example:

BRANHARD 25

THE FIRST COLLECTION

WE DON'T FOLLOW TRENDS.
WE BUILD IDENTITY.

SHOP THE COLLECTION

Do not hard-code this text if the existing application already has editable content.

The hero should feel like a fashion campaign rather than a normal ecommerce banner.

---

## 4. Featured Collection

After the hero, create a large editorial section.

Include:

- Large campaign image
- Collection title
- Short description
- CTA

Use generous spacing.

---

## 5. Product Categories

Create visual category sections for:

- T-Shirts
- Hoodies
- Joggers
- Jackets
- Accessories

Each category should contain:

- Image
- Category name
- Short description
- Shop CTA

Use large imagery rather than small generic cards.

---

## 6. Featured Products

Create a premium product grid.

Desktop:

4 columns where appropriate.

Tablet:

2–3 columns.

Mobile:

2 columns when readable, otherwise 1 column.

Each product card should contain:

- Product image
- Product name
- Price
- Available variants where supported
- Availability where supported
- Quick add only if the existing ecommerce system supports it

Avoid excessive card borders.

---

## 7. Brand Story

Create an editorial BRANHARD story section.

Use:

- Large typography
- Strong photography
- Short copy
- Clear visual hierarchy

The section should communicate the identity of BRANHARD without becoming a large block of text.

---

## 8. Campaign / Lookbook

Create a large visual campaign section.

Possible links:

- Explore Collection
- Lookbook
- Latest Drop
- Campaign

This section should visually break up the product sections.

---

## 9. Newsletter

Create a simple newsletter/community section.

Example:

JOIN THE BRANHARD WORLD

Be first to know about new collections, drops and campaigns.

Keep the form simple.

---

## 10. Footer

Include:

- Shop
- Collections
- About
- Contact
- Shipping
- Returns
- Privacy
- Terms
- Social links

Keep the footer clean and premium.

---

# VISUAL SYSTEM

## Colors

Primary direction:

- Black
- White
- Charcoal
- Warm neutrals

Use existing BRANHARD accent colors when they already exist in the project.

Do not introduce random colors.

## Typography

Use the existing BRANHARD typography system if available.

If none exists:

- Editorial display typography for major headings
- Clean sans-serif for navigation and ecommerce UI

Do not use too many font families.

## Spacing

Use generous whitespace.

Sections should breathe.

Do not overcrowd the viewport.

---

# ANIMATION

Use subtle animation only.

Allowed:

- Fade-in
- Gentle image reveal
- Slow image scale
- Product hover image
- Smooth carousel

Avoid:

- Excessive bouncing
- Distracting effects
- Long blocking animations
- Animation that prevents shopping

Respect:

prefers-reduced-motion

---

# RESPONSIVE DESIGN

Test:

360px
390px
430px
768px
1024px
1440px

The mobile version must be intentionally designed.

Do not simply shrink the desktop layout.

---

# PERFORMANCE

The implementation should:

- Lazy-load below-the-fold images
- Use responsive image sizes
- Avoid unnecessary JavaScript
- Avoid multiple large videos loading simultaneously
- Provide image fallbacks
- Prevent layout shift
- Keep the homepage fast

---

# ACCESSIBILITY

Every meaningful image requires appropriate alt text.

Interactive controls require accessible labels.

Maintain readable contrast.

Keyboard navigation should work.

Do not communicate important information through color alone.

---

# ECOMMERCE SAFETY

Before changing the homepage:

1. Inspect the existing application.
2. Identify the current homepage entry point.
3. Identify existing components.
4. Identify existing product data.
5. Identify existing cart functionality.
6. Identify existing checkout functionality.
7. Identify existing payment integration.

Never delete working ecommerce functionality simply to redesign the homepage.

---

# ADMIN / CONTENT EDITABILITY

Where an admin or CMS system already exists, homepage content should be editable.

Potential editable fields:

- Hero image/video
- Hero heading
- Hero description
- Hero CTA
- Featured collection
- Category images
- Featured products
- Campaign sections
- Announcement bar

---

# IMPLEMENTATION RULES

1. Inspect before editing.
2. Reuse existing components when practical.
3. Do not rebuild the entire application unnecessarily.
4. Preserve existing APIs.
5. Preserve cart functionality.
6. Preserve checkout.
7. Preserve payment integrations.
8. Keep components modular.
9. Keep content separate from layout where practical.
10. Test every major section.
11. Test mobile and desktop.
12. Fix console errors.
13. Fix broken links.
14. Never expose API keys.
15. Do not modify .env files unless explicitly required.
16. Do not remove existing working features without approval.

---

# QA CHECKLIST

Before declaring the homepage complete:

[ ] Homepage loads
[ ] No console errors
[ ] Navigation works
[ ] Mobile navigation works
[ ] Hero loads correctly
[ ] Hero CTA works
[ ] Product cards work
[ ] Product links work
[ ] Cart works
[ ] Search works
[ ] Images load
[ ] No horizontal overflow
[ ] Responsive layout works
[ ] No broken links
[ ] No API keys exposed
[ ] Existing payment system remains intact
[ ] Existing product data remains intact
[ ] Accessibility basics checked
[ ] Performance checked

---

# WORKFLOW INTEGRATION

When this skill is used by the BRANHARD AI workflow:

CHATGPT
→ Creates homepage plan

GEMINI / DEEPSEEK / GROK
→ Research and critique design approaches

CHATGPT
→ Decides the implementation direction

CLAUDE
→ Implements the homepage

TEST
→ Verifies the implementation

GITHUB
→ Saves the approved changes

JOURNAL
→ Records the task and result

---

# DEFINITION OF DONE

The homepage is complete when:

- It has a premium BRANHARD editorial fashion appearance.
- It follows the supplied BRANHARD wireframe.
- It follows the supplied visual direction.
- It works on mobile and desktop.
- Ecommerce functionality remains intact.
- Product data remains intact.
- Navigation works.
- Cart and checkout remain functional.
- The homepage has no critical console errors.
- The implementation is responsive.
- Performance and accessibility basics are addressed.
- The workflow journal records the implementation.

