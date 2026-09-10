// Static content (curriculum data is baked in at build time, progress
// state is client-only localStorage). Prerender to a static document so
// it is served straight from the CDN edge: no SSR invocation, ~0 TTFB.
export const prerender = true;
