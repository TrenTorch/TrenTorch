// Every route is static content (the curriculum is baked in at build time,
// progress and auth state live client-side). Prerendering at the root
// guarantees each page is a real .html file: without it, a route with no
// +page.ts of its own is only reachable through the SPA fallback, which a
// static host serves with a 404 status that search engines will not index.
export const prerender = true;
