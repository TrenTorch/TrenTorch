
import root from '../root.js';
import { set_building, set_prerendering } from '$app/env/internal';
import { set_assets } from '$app/paths/internal/server';
import { set_manifest, set_read_implementation } from '__sveltekit/server';
import { set_private_env, set_public_env } from '../../../node_modules/@sveltejs/kit/src/runtime/shared-server.js';
import error from '../shared/error-template.js';

export const options = {
	app_template_contains_nonce: false,
	async: false,
	csp: {"mode":"auto","directives":{"upgrade-insecure-requests":false,"block-all-mixed-content":false},"reportOnly":{"upgrade-insecure-requests":false,"block-all-mixed-content":false}},
	csrf_check_origin: true,
	csrf_trusted_origins: [],
	embedded: false,
	env_public_prefix: 'PUBLIC_',
	env_private_prefix: '',
	hash_routing: false,
	hooks: null, // added lazily, via `get_hooks`
	preload_strategy: "modulepreload",
	root,
	service_worker: true,
	service_worker_options: undefined,
	server_error_boundaries: false,
	templates: {
		app: ({ head, body, assets, nonce, env }) => "<!doctype html>\n<html lang=\"en\">\n\t<head>\n\t\t<meta charset=\"utf-8\" />\n\t\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n\t\t<meta name=\"text-scale\" content=\"scale\" />\n\t\t<!-- Fonts are self-hosted and Vite-fingerprinted (@font-face in\n\t\t     layout.css, files in src/lib/fonts); the @font-face rule ships in\n\t\t     the layout stylesheet, so the fetch starts as soon as that CSS\n\t\t     parses, with no round-trip to fonts.googleapis.com and no second\n\t\t     connection to fonts.gstatic.com. -->\n\t\t<!-- The IDE's Python runtime streams from this CDN on first Run/Submit;\n\t\t     warm the connection early so the 7.8 MB transfer isn't also paying\n\t\t     DNS + TLS when it starts. -->\n\t\t<link rel=\"preconnect\" href=\"https://cdn.jsdelivr.net\" crossorigin=\"anonymous\" />\n\t\t<script>\n\t\t\t// Applied before hydration so there's no flash of the wrong theme:\n\t\t\t// mirrors what a client-side toggle would do, but runs synchronously\n\t\t\t// as the very first thing in <head>.\n\t\t\ttry {\n\t\t\t\tconst stored = localStorage.getItem('theme');\n\t\t\t\tconst dark = stored\n\t\t\t\t\t? stored === 'dark'\n\t\t\t\t\t: window.matchMedia('(prefers-color-scheme: dark)').matches;\n\t\t\t\tdocument.documentElement.classList.toggle('dark', dark);\n\t\t\t} catch {\n\t\t\t\t// localStorage unavailable (private mode, disabled storage): fall\n\t\t\t\t// back to light, same as a fresh visitor with no stored preference.\n\t\t\t}\n\t\t</script>\n\t\t" + head + "\n\t</head>\n\t<body data-sveltekit-preload-data=\"hover\">\n\t\t<div style=\"display: contents\">" + body + "</div>\n\t</body>\n</html>\n",
		error
	},
	version_hash: "ha4lj2"
};

export async function get_hooks() {
	let handle;
	let handleFetch;
	let handleError;
	let handleValidationError;
	let init;
	

	let reroute;
	let transport;
	

	return {
		handle,
		handleFetch,
		handleError,
		handleValidationError,
		init,
		reroute,
		transport
	};
}

export { set_assets, set_building, set_manifest, set_prerendering, set_private_env, set_public_env, set_read_implementation };
