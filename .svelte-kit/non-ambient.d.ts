
// this file is generated — do not edit it


declare module "svelte/elements" {
	export interface HTMLAttributes<T> {
		'data-sveltekit-keepfocus'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-noscroll'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-preload-code'?:
			| true
			| ''
			| 'eager'
			| 'viewport'
			| 'hover'
			| 'tap'
			| 'off'
			| undefined
			| null;
		'data-sveltekit-preload-data'?: true | '' | 'hover' | 'tap' | 'off' | undefined | null;
		'data-sveltekit-reload'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-replacestate'?: true | '' | 'off' | undefined | null;
	}
}

export {};


declare module "$app/types" {
	type MatcherParam<M> = M extends (param : string) => param is (infer U extends string) ? U : string;

	export interface AppTypes {
		RouteId(): "/" | "/account" | "/contact" | "/ide" | "/ide/[id]" | "/potd" | "/privacy" | "/questions" | "/questions/[partId]" | "/terms";
		RouteParams(): {
			"/ide/[id]": { id: string };
			"/questions/[partId]": { partId: string }
		};
		LayoutParams(): {
			"/": { id?: string | undefined; partId?: string | undefined };
			"/account": Record<string, never>;
			"/contact": Record<string, never>;
			"/ide": { id?: string | undefined };
			"/ide/[id]": { id: string };
			"/potd": Record<string, never>;
			"/privacy": Record<string, never>;
			"/questions": { partId?: string | undefined };
			"/questions/[partId]": { partId: string };
			"/terms": Record<string, never>
		};
		Pathname(): "/" | "/account" | "/contact" | `/ide/${string}` & {} | `/ide/${string}/` & {} | "/potd" | "/privacy" | "/questions" | `/questions/${string}` & {} | `/questions/${string}/` & {} | "/terms";
		ResolvedPathname(): `${"" | `/${string}`}${ReturnType<AppTypes['Pathname']>}`;
		Asset(): "/funding.json" | "/robots.txt" | "/testimonial-screenshots/anushka.webp" | "/testimonial-screenshots/athrix.webp" | "/testimonial-screenshots/avrl.webp" | "/testimonial-screenshots/divyansh.webp" | "/testimonial-screenshots/harsh-jain.webp" | "/testimonial-screenshots/harsh.webp" | "/testimonial-screenshots/harshit.webp" | "/testimonial-screenshots/mitali.webp" | "/testimonial-screenshots/patnayak.webp" | "/testimonial-screenshots/shreya.webp" | "/testimonial-screenshots/simran.webp" | "/testimonial-screenshots/tannu.webp" | "/testimonial-screenshots/unmesh.webp" | "/testimonial-screenshots/vaibhav.webp" | "/testimonial-screenshots/yug.webp" | string & {};
	}
}