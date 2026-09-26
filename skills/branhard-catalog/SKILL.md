# BRANHARD CATALOG SKILL

## Purpose

Build and maintain the BRANHARD catalog page as a premium, modern streetwear shopping experience.

The catalog should feel consistent with the BRANHARD brand and the overall website design.

## Core Responsibilities

- Display products clearly and consistently.
- Support product categories.
- Support search and filtering.
- Support sorting.
- Show product images, names, prices, colors, sizes, availability, and descriptions.
- Provide clear product navigation.
- Maintain a premium streetwear aesthetic.
- Work well on mobile and desktop.
- Keep the interface fast and easy to navigate.

## Product Data

Always use the application's real product data.

Never invent:

- Prices
- Stock
- Sizes
- Colors
- Product names
- Product IDs

If the existing API or database supplies the information, use it.

## Catalog Structure

The catalog should support categories such as:

- Hoodies
- T-Shirts
- Polo
- Pants
- Joggers
- Jackets
- Bags
- Caps
- Accessories

## Search and Filter State

Where practical, preserve catalog state in the URL.

Examples:

/catalog?category=hoodies

/catalog?sort=newest

/catalog?search=essential

/catalog?category=tshirts&color=black

## Product Cards

Each product card should provide:

- Product image
- Product name
- Short description
- Price
- Available colors
- Availability
- Product link

Use high-quality imagery and consistent image proportions.

## Product Page Navigation

Clicking a product should open its product page.

The product page should provide:

- Product gallery
- Product title
- Description
- Price
- Size selection
- Color selection
- Availability
- Reviews when available
- Add to cart
- Wishlist when supported
- Delivery information

## Design Direction

Use a premium BRANHARD streetwear aesthetic.

Design principles:

- Strong typography
- Clean spacing
- High-quality product photography
- Minimal unnecessary decoration
- Strong visual hierarchy
- Premium editorial feel
- Responsive layout
- Smooth interactions
- Clear calls to action

The catalog should feel like a serious fashion-commerce website rather than a generic online store.

## Mobile Experience

Prioritize mobile usability.

The catalog should:

- Load quickly
- Use responsive product grids
- Keep filters accessible
- Keep search easy to access
- Make product cards easy to tap
- Avoid unnecessary horizontal scrolling
- Maintain readable typography

## Performance

Avoid unnecessary API requests.

Use:

- Lazy-loaded product images
- Efficient data fetching
- Cached catalog data where appropriate
- Pagination or controlled loading for large catalogs

## Accessibility

Use:

- Accessible buttons
- Meaningful image alt text
- Keyboard navigation
- Visible focus states
- Sufficient text contrast
- Clear form labels

## Error Handling

If catalog data cannot be loaded:

- Show a clear loading state.
- Show a useful error message.
- Provide a retry action.
- Never display fabricated product information.

## Agent Behavior

When modifying the catalog:

1. Inspect the existing application structure.
2. Reuse existing components where possible.
3. Preserve existing functionality.
4. Use the existing product data source.
5. Avoid breaking checkout, cart, search, or product pages.
6. Test the catalog after changes.
7. Report exactly what was changed.
8. Do not claim a feature works unless it has been tested.

## Completion Criteria

The catalog skill is complete when:

- Products display correctly.
- Categories work.
- Search works.
- Filters work.
- Sorting works.
- Product links work.
- Real product data is used.
- Mobile layout works.
- Desktop layout works.
- Loading and error states work.
- No existing shopping functionality is broken.
