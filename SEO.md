# Search discoverability — 7 September 2026

Implemented for the local production build:

- Home-page `WebSite` markup identifies the preferred site name, León Palafox, and its unaccented variant.
- About-page `ProfilePage` markup connects the profile to the same person referenced by articles. The visible heading now includes the full name.
- Article markup explicitly identifies the author and links to the About page. Every article has a visible linked byline.
- Breadcrumb navigation and matching `BreadcrumbList` markup connect pages to Home, Blog, or Teaching.
- Articles link to up to three other articles in the same language, prioritizing shared tags and then publication date.
- Teaching demos have descriptive search titles: Interactive Regression Uncertainty and Interactive Schelling Segregation Model.
- Indexable pages permit large image previews. Existing descriptions, canonical links, article dates, language metadata, and the 404 noindex directive remain in place.
- Course links stay on the current site during local previews.

Validation: production build passes; all 32 indexable pages have unique canonical URLs and are present in the sitemap. Structured-data JSON, breadcrumb positions and local targets, and article author links pass local checks. All 790 relative local references across 54 generated HTML files resolve. Chrome also passed 44 responsive checks across four widths, and automated accessibility scans passed on 11 representative routes. These checks are not a Google Rich Results Test or proof of indexing.

The public robots.txt and both sitemap files return HTTP 200. Public robots.txt allows crawling and advertises the sitemap. Google Search Console indexing and search-performance reports were not accessed.

## After deployment

In the owner's Google Search Console property, submit `https://www.leonpalafox.com/sitemap-index.xml` if it is not already submitted. Inspect the homepage, About page, and a recent article, and request indexing if appropriate. Validate the deployed structured data with Google's Rich Results Test. Monitor indexing and actual search impressions afterward; these local changes do not establish any ranking improvement.

No sitemap submission, indexing request, or public deployment was performed. No artificial modification dates, hidden keywords, or unverified biographical claims were added.

## References

These changes follow Google's guidance on [site names](https://developers.google.com/search/docs/appearance/site-names), [profile pages](https://developers.google.com/search/docs/appearance/structured-data/profile-page), [article authors](https://developers.google.com/search/docs/appearance/structured-data/article), and [breadcrumbs](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb). Google describes how crawlable links, descriptive content, and metadata help discovery in its [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide).
