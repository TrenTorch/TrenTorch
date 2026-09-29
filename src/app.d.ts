// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}

	interface Window {
		turnstile: {
			render: (
				container: HTMLElement,
				options: {
					sitekey: string;
					action?: string;
					callback?: (token: string) => void;
					'expired-callback'?: () => void;
				}
			) => string;
			reset: (widgetId: string) => void;
		};
	}
}

export {};
