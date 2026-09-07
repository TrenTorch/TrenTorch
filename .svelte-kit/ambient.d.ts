
// this file is generated — do not edit it


/// <reference types="@sveltejs/kit" />

/**
 * This module provides access to environment variables that are injected _statically_ into your bundle at build time and are limited to _private_ access.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Static environment variables are [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env` at build time and then statically injected into your bundle at build time, enabling optimisations like dead code elimination.
 * 
 * **_Private_ access:**
 * 
 * - This module cannot be imported into client-side code
 * - This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured)
 * 
 * For example, given the following build time environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://site.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { ENVIRONMENT, PUBLIC_BASE_URL } from '$env/static/private';
 * 
 * console.log(ENVIRONMENT); // => "production"
 * console.log(PUBLIC_BASE_URL); // => throws error during build
 * ```
 * 
 * The above values will be the same _even if_ different values for `ENVIRONMENT` or `PUBLIC_BASE_URL` are set at runtime, as they are statically replaced in your code with their build time values.
 */
declare module '$env/static/private' {
	export const SHELL: string;
	export const npm_command: string;
	export const npm_config_userconfig: string;
	export const COLORTERM: string;
	export const npm_config_cache: string;
	export const HISTCONTROL: string;
	export const XDG_MENU_PREFIX: string;
	export const QT_IM_MODULES: string;
	export const HISTSIZE: string;
	export const HOSTNAME: string;
	export const NODE: string;
	export const SSH_AUTH_SOCK: string;
	export const MEMORY_PRESSURE_WRITE: string;
	export const COLOR: string;
	export const npm_config_local_prefix: string;
	export const XMODIFIERS: string;
	export const DESKTOP_SESSION: string;
	export const KITTY_PID: string;
	export const npm_config_globalconfig: string;
	export const GPG_TTY: string;
	export const EDITOR: string;
	export const PWD: string;
	export const LOGNAME: string;
	export const XDG_SESSION_DESKTOP: string;
	export const XDG_SESSION_TYPE: string;
	export const npm_config_init_module: string;
	export const SYSTEMD_EXEC_PID: string;
	export const VECDB_URL: string;
	export const _: string;
	export const XAUTHORITY: string;
	export const DESKTOP_STARTUP_ID: string;
	export const SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS: string;
	export const KITTY_PUBLIC_KEY: string;
	export const GJS_DEBUG_TOPICS: string;
	export const API_KEY: string;
	export const GDM_LANG: string;
	export const HOME: string;
	export const USERNAME: string;
	export const LANG: string;
	export const LS_COLORS: string;
	export const XDG_CURRENT_DESKTOP: string;
	export const npm_package_version: string;
	export const MEMORY_PRESSURE_WATCH: string;
	export const WAYLAND_DISPLAY: string;
	export const KITTY_WINDOW_ID: string;
	export const INVOCATION_ID: string;
	export const MANAGERPID: string;
	export const INIT_CWD: string;
	export const STEAM_FRAME_FORCE_CLOSE: string;
	export const npm_lifecycle_script: string;
	export const GJS_DEBUG_OUTPUT: string;
	export const GNOME_SETUP_DISPLAY: string;
	export const npm_config_npm_version: string;
	export const XDG_SESSION_CLASS: string;
	export const TERM: string;
	export const TERMINFO: string;
	export const npm_package_name: string;
	export const npm_config_prefix: string;
	export const LESSOPEN: string;
	export const USER: string;
	export const DISPLAY: string;
	export const npm_lifecycle_event: string;
	export const SHLVL: string;
	export const QT_IM_MODULE: string;
	export const MANAGERPIDFDID: string;
	export const npm_config_user_agent: string;
	export const npm_execpath: string;
	export const XDG_RUNTIME_DIR: string;
	export const DEBUGINFOD_URLS: string;
	export const npm_package_json: string;
	export const DEBUGINFOD_IMA_CERT_PATH: string;
	export const JOURNAL_STREAM: string;
	export const XDG_DATA_DIRS: string;
	export const npm_config_noproxy: string;
	export const PATH: string;
	export const npm_config_node_gyp: string;
	export const GDMSESSION: string;
	export const XDG_SESSION_EXTRA_DEVICE_ACCESS: string;
	export const DBUS_SESSION_BUS_ADDRESS: string;
	export const npm_config_global_prefix: string;
	export const npm_config_update_notifier: string;
	export const MAIL: string;
	export const KITTY_INSTALLATION_DIR: string;
	export const GIO_LAUNCHED_DESKTOP_FILE_PID: string;
	export const npm_node_execpath: string;
	export const npm_config_engine_strict: string;
	export const GIO_LAUNCHED_DESKTOP_FILE: string;
	export const OLDPWD: string;
	export const NODE_ENV: string;
}

/**
 * This module provides access to environment variables that are injected _statically_ into your bundle at build time and are _publicly_ accessible.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Static environment variables are [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env` at build time and then statically injected into your bundle at build time, enabling optimisations like dead code elimination.
 * 
 * **_Public_ access:**
 * 
 * - This module _can_ be imported into client-side code
 * - **Only** variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`) are included
 * 
 * For example, given the following build time environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://site.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { ENVIRONMENT, PUBLIC_BASE_URL } from '$env/static/public';
 * 
 * console.log(ENVIRONMENT); // => throws error during build
 * console.log(PUBLIC_BASE_URL); // => "http://site.com"
 * ```
 * 
 * The above values will be the same _even if_ different values for `ENVIRONMENT` or `PUBLIC_BASE_URL` are set at runtime, as they are statically replaced in your code with their build time values.
 */
declare module '$env/static/public' {
	export const PUBLIC_SUPABASE_ANON_KEY: string;
	export const PUBLIC_SUPABASE_URL: string;
}

/**
 * This module provides access to environment variables set _dynamically_ at runtime and that are limited to _private_ access.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Dynamic environment variables are defined by the platform you're running on. For example if you're using [`adapter-node`](https://github.com/sveltejs/kit/tree/main/packages/adapter-node) (or running [`vite preview`](https://svelte.dev/docs/kit/cli)), this is equivalent to `process.env`.
 * 
 * **_Private_ access:**
 * 
 * - This module cannot be imported into client-side code
 * - This module includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured)
 * 
 * > [!NOTE] In `dev`, `$env/dynamic` includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.
 * 
 * > [!NOTE] To get correct types, environment variables referenced in your code should be declared (for example in an `.env` file), even if they don't have a value until the app is deployed:
 * >
 * > ```env
 * > MY_FEATURE_FLAG=
 * > ```
 * >
 * > You can override `.env` values from the command line like so:
 * >
 * > ```sh
 * > MY_FEATURE_FLAG="enabled" npm run dev
 * > ```
 * 
 * For example, given the following runtime environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://site.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { env } from '$env/dynamic/private';
 * 
 * console.log(env.ENVIRONMENT); // => "production"
 * console.log(env.PUBLIC_BASE_URL); // => undefined
 * ```
 */
declare module '$env/dynamic/private' {
	export const env: {
		SHELL: string;
		npm_command: string;
		npm_config_userconfig: string;
		COLORTERM: string;
		npm_config_cache: string;
		HISTCONTROL: string;
		XDG_MENU_PREFIX: string;
		QT_IM_MODULES: string;
		HISTSIZE: string;
		HOSTNAME: string;
		NODE: string;
		SSH_AUTH_SOCK: string;
		MEMORY_PRESSURE_WRITE: string;
		COLOR: string;
		npm_config_local_prefix: string;
		XMODIFIERS: string;
		DESKTOP_SESSION: string;
		KITTY_PID: string;
		npm_config_globalconfig: string;
		GPG_TTY: string;
		EDITOR: string;
		PWD: string;
		LOGNAME: string;
		XDG_SESSION_DESKTOP: string;
		XDG_SESSION_TYPE: string;
		npm_config_init_module: string;
		SYSTEMD_EXEC_PID: string;
		VECDB_URL: string;
		_: string;
		XAUTHORITY: string;
		DESKTOP_STARTUP_ID: string;
		SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS: string;
		KITTY_PUBLIC_KEY: string;
		GJS_DEBUG_TOPICS: string;
		API_KEY: string;
		GDM_LANG: string;
		HOME: string;
		USERNAME: string;
		LANG: string;
		LS_COLORS: string;
		XDG_CURRENT_DESKTOP: string;
		npm_package_version: string;
		MEMORY_PRESSURE_WATCH: string;
		WAYLAND_DISPLAY: string;
		KITTY_WINDOW_ID: string;
		INVOCATION_ID: string;
		MANAGERPID: string;
		INIT_CWD: string;
		STEAM_FRAME_FORCE_CLOSE: string;
		npm_lifecycle_script: string;
		GJS_DEBUG_OUTPUT: string;
		GNOME_SETUP_DISPLAY: string;
		npm_config_npm_version: string;
		XDG_SESSION_CLASS: string;
		TERM: string;
		TERMINFO: string;
		npm_package_name: string;
		npm_config_prefix: string;
		LESSOPEN: string;
		USER: string;
		DISPLAY: string;
		npm_lifecycle_event: string;
		SHLVL: string;
		QT_IM_MODULE: string;
		MANAGERPIDFDID: string;
		npm_config_user_agent: string;
		npm_execpath: string;
		XDG_RUNTIME_DIR: string;
		DEBUGINFOD_URLS: string;
		npm_package_json: string;
		DEBUGINFOD_IMA_CERT_PATH: string;
		JOURNAL_STREAM: string;
		XDG_DATA_DIRS: string;
		npm_config_noproxy: string;
		PATH: string;
		npm_config_node_gyp: string;
		GDMSESSION: string;
		XDG_SESSION_EXTRA_DEVICE_ACCESS: string;
		DBUS_SESSION_BUS_ADDRESS: string;
		npm_config_global_prefix: string;
		npm_config_update_notifier: string;
		MAIL: string;
		KITTY_INSTALLATION_DIR: string;
		GIO_LAUNCHED_DESKTOP_FILE_PID: string;
		npm_node_execpath: string;
		npm_config_engine_strict: string;
		GIO_LAUNCHED_DESKTOP_FILE: string;
		OLDPWD: string;
		NODE_ENV: string;
		[key: `PUBLIC_${string}`]: undefined;
		[key: `${string}`]: string | undefined;
	}
}

/**
 * This module provides access to environment variables set _dynamically_ at runtime and that are _publicly_ accessible.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Dynamic environment variables are defined by the platform you're running on. For example if you're using [`adapter-node`](https://github.com/sveltejs/kit/tree/main/packages/adapter-node) (or running [`vite preview`](https://svelte.dev/docs/kit/cli)), this is equivalent to `process.env`.
 * 
 * **_Public_ access:**
 * 
 * - This module _can_ be imported into client-side code
 * - **Only** variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`) are included
 * 
 * > [!NOTE] In `dev`, `$env/dynamic` includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.
 * 
 * > [!NOTE] To get correct types, environment variables referenced in your code should be declared (for example in an `.env` file), even if they don't have a value until the app is deployed:
 * >
 * > ```env
 * > MY_FEATURE_FLAG=
 * > ```
 * >
 * > You can override `.env` values from the command line like so:
 * >
 * > ```sh
 * > MY_FEATURE_FLAG="enabled" npm run dev
 * > ```
 * 
 * For example, given the following runtime environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://example.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { env } from '$env/dynamic/public';
 * console.log(env.ENVIRONMENT); // => undefined, not public
 * console.log(env.PUBLIC_BASE_URL); // => "http://example.com"
 * ```
 * 
 * ```
 * 
 * ```
 */
declare module '$env/dynamic/public' {
	export const env: {
		PUBLIC_SUPABASE_ANON_KEY: string;
		PUBLIC_SUPABASE_URL: string;
		[key: `PUBLIC_${string}`]: string | undefined;
	}
}
