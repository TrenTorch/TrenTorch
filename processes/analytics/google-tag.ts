// The Google tag itself lives in platform/app.html. This only sends custom
// events through the global gtag it defines, and does nothing if the tag is
// missing (dev, tests, ad blockers).
type GtagWindow = Window & { gtag?: (...args: unknown[]) => void };

/** Custom event with small, non personal parameters (a question id, a result). */
export function trackEvent(name: string, params: Record<string, string | number | boolean> = {}) {
	if (typeof window === 'undefined') return;
	(window as GtagWindow).gtag?.('event', name, params);
}
