// Google Analytics 4 through gtag.js. Inert unless a production build has
// VITE_GA_MEASUREMENT_ID set (for example G-XXXXXXXXXX), so dev, previews and
// tests never send data and nothing loads without an ID.
const MEASUREMENT_ID: string | undefined = import.meta.env.VITE_GA_MEASUREMENT_ID;

type Gtag = (...args: unknown[]) => void;
type GtagWindow = Window & { dataLayer?: unknown[]; gtag?: Gtag };

let loaded = false;

export const analyticsEnabled = (): boolean =>
	import.meta.env.PROD &&
	typeof window !== 'undefined' &&
	/^G-[A-Z0-9]+$/.test(MEASUREMENT_ID ?? '');

/** Adds gtag.js once. Page views are sent by trackPageView, not automatically,
 * because the site is a single page app and route changes are not page loads. */
export function loadGoogleTag(): void {
	if (loaded || !analyticsEnabled()) return;
	loaded = true;
	const w = window as GtagWindow;
	w.dataLayer = w.dataLayer || [];
	w.gtag = function () {
		// gtag.js reads the arguments object itself, an array would not work.
		// eslint-disable-next-line prefer-rest-params
		w.dataLayer!.push(arguments);
	};
	w.gtag('js', new Date());
	w.gtag('config', MEASUREMENT_ID, { send_page_view: false });
	const script = document.createElement('script');
	script.async = true;
	script.src = `https://www.googletagmanager.com/gtag/js?id=${MEASUREMENT_ID}`;
	document.head.appendChild(script);
}

export function trackPageView(path: string): void {
	if (!loaded) return;
	(window as GtagWindow).gtag?.('event', 'page_view', {
		page_path: path,
		page_location: window.location.href,
		page_title: document.title
	});
}

/** Custom event with small, non personal parameters (a question id, a result). */
export function trackEvent(name: string, params: Record<string, string | number | boolean> = {}) {
	if (!loaded) return;
	(window as GtagWindow).gtag?.('event', name, params);
}
