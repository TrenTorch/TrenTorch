// The username is only known at request time, so this page is not prerendered.
// The static host serves the app shell for /accounts/@name and this route
// fills it in on the client.
export const prerender = false;
