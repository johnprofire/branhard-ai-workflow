# BRANHARD Catalog Page Skill

## Purpose
Design, build, review, and improve the BRANHARD catalog/shop page in code.

The catalog should feel premium, editorial, modern, minimal, fashion-focused, streetwear-focused, easy to shop, and mobile-first.

Do not copy another company's branding, logo, wording, images, or proprietary implementation.

## Catalog Structure

### Catalog Header
Include:
- BRANHARD catalog/shop title
- Optional short description
- Product count when available

Keep the header spacious and editorial.

### Category Navigation
Use real categories from product data, such as:
- All
- T-Shirts
- Hoodies
- Joggers
- Jackets
- Pants
- Accessories
- New Arrivals
- Collections

Do not create categories with no products.

### Search
Provide fast product search using the existing search system where one exists.

### Filters
Where supported by real product data:
- Category
- Size
- Color
- Price
- Collection
- Availability

Desktop can use a sidebar or horizontal controls. Mobile should use a clean filter drawer/panel.

### Sorting
Where supported:
- Featured
- Newest
- Price: Low to High
- Price: High to Low

Only show options that can actually be implemented correctly.

### Product Grid
Desktop: 4 columns where appropriate.
Tablet: 2–3 columns.
Mobile: 2 columns when readable, otherwise 1.

Maintain consistent image proportions and generous spacing.

### Product Cards
Use:
- Product image
- Product name
- Price
- Variants where useful
- Availability where supported

Optional:
- Quick Add
- Wishlist
- Secondary image on hover

Do not overcrowd cards.

### Product Images
Use real project product imagery. Images should be high quality, consistent, optimized, responsive, and have appropriate alt text.

### Product States
Handle real states correctly:
- Available
- Low stock when supported by inventory
- Sold out
- Sale pricing when supported
- New label when supported

Never invent product data.

## Mobile Experience
Design mobile intentionally:

Header
→ Category navigation
→ Search
→ Filter / Sort
→ Product grid

Controls and product images must remain easy to use on phones.

## Desktop Experience
Recommended:

Top navigation
→ Catalog heading
→ Categories
→ Search / Filter / Sort
→ Large product grid

Use generous whitespace.

## Visual System

Primary BRANHARD direction:
- Black
- White
- Charcoal
- Warm neutrals

Use existing BRANHARD accent colors where already defined.

Use the existing BRANHARD typography system. If none exists, use editorial display typography for major headings and a clean sans-serif for UI and product information.

## Motion
Use subtle image fades, image swaps, gentle hover effects, filter-drawer transitions, and smooth transitions.

Avoid distracting or shopping-blocking animation.

Respect `prefers-reduced-motion`.

## Cart Integration
Use the existing cart system. Do not create a separate cart.

If Quick Add exists:
1. Use the existing cart API/state.
2. Confirm the action visually.
3. Keep the customer on the catalog when appropriate.

If a product requires a size or variant, do not add an ambiguous variant automatically.

## Product Data
Always use real application product data.

Never invent:
- Prices
- Stock
- Sizes
- Colors
- Product names
- Product IDs

## URL State
Where practical, preserve catalog state in the URL.

Examples:

```text
/catalog?category=hoodies
/catalog?sort=newest
/catalog?search=essential
/catalog?category=tshirts&color=black
```

Use the application's existing routing system.

## Performance
- Lazy-load below-the-fold product images
- Use responsive image sizes
- Use pagination or controlled loading
- Avoid unnecessary JavaScript
- Avoid loading hundreds of products at once

## Accessibility
Support:
- Keyboard navigation
- Screen-reader labels
- Accessible filters
- Accessible search
- Visible focus states
- Sufficient contrast
- Descriptive image alt text

Do not rely on color alone for important information.

## Responsive Testing
Test at:
- 360px
- 390px
- 430px
- 768px
- 1024px
- 1440px

Check for no horizontal overflow, usable images, working filters/search/sorting/navigation/cart/product links.

## Implementation Rules
Before modifying the catalog:
1. Inspect the existing application.
2. Identify the catalog route/page.
3. Identify the product data source.
4. Identify the product card component.
5. Identify the cart implementation.
6. Identify search and filter implementations.
7. Identify checkout implementation.
8. Reuse existing infrastructure where practical.
9. Do not delete working ecommerce functionality.
10. Do not replace working APIs without approval.
11. Do not expose API keys.
12. Do not modify `.env` unless explicitly required.

## Admin / Content Editability
If the project has an admin system, keep catalog content editable.

Possible editable data:
- Products
- Categories
- Prices
- Images
- Product descriptions
- Availability
- Collections
- Featured status

The catalog should consume this data instead of hard-coding products.

## QA Checklist
- [ ] Catalog loads
- [ ] No console errors
- [ ] Product data loads
- [ ] Product images load
- [ ] Categories work
- [ ] Search works
- [ ] Filters work where supported
- [ ] Sorting works where supported
- [ ] Product links work
- [ ] Product details work
- [ ] Cart integration works
- [ ] Variant selection works
- [ ] Sold-out state works
- [ ] Sale pricing works where applicable
- [ ] Mobile layout works
- [ ] Desktop layout works
- [ ] No horizontal overflow
- [ ] No broken links
- [ ] No API keys exposed
- [ ] Accessibility basics checked
- [ ] Performance checked

## Workflow Integration
ChatGPT → Catalog implementation plan

Gemini → Alternative UX/design analysis

DeepSeek → Technical/product-catalog analysis

Grok → Design and implementation review

ChatGPT → Implementation decision

Claude → Implementation

Test → Verification

GitHub → Save approved changes

Journal → Record the workflow and result

## Definition of Done
The BRANHARD catalog is complete when it has a premium BRANHARD visual identity, real product data, working categories/search/filters/sorting where supported, responsive product images, working cart and product links, no critical console errors, no exposed secrets, accessibility basics, acceptable performance, and a journal record of the completed task.
