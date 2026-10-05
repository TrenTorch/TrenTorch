/// <reference types="@sveltejs/kit" />
/// <reference lib="webworker" />

import { build, files, version } from '$service-worker';

// Two jobs:
//  1. App shell: precache this build's hashed JS/CSS/fonts on install and
//     serve them cache-first. They're content-hashed, so a cache hit is
//     always correct; a returning visitor fetches nothing from the host.
//     HTML/navigations use stale-while-revalidate: instant from cache,
//     refreshed in the background.
//  2. Pyodide runtime (CPython + NumPy, ~7.8 MB from jsDelivr): a
//     dedicated, version-pinned cache so it's a genuine one-time download
//     that survives HTTP-cache eviction and works offline.
//  3. The self-hosted Python wheels (seaborn, plotly, narwhals under /wheels/): not
//     precached, since most visitors never open a question that needs them, but
//     cached the first time one is fetched, so later visits and offline use are local.
// Anything else passes straight through to the network.

const sw = self as unknown as ServiceWorkerGlobalScope;

const APP_CACHE = `app-${version}`;
const PYODIDE_CACHE = 'pyodide-v0.27.2';
const PYODIDE_ORIGIN = 'https://cdn.jsdelivr.net';
const PYODIDE_PATH = '/pyodide/v0.27.2/';
const WHEELS_CACHE = 'wheels-v1';
const WHEELS_SEGMENT = '/wheels/';

// The wheels are large and only some questions need them: leave them out of the install-time precache.
const PRECACHE = [...build, ...files.filter((file) => !file.includes(WHEELS_SEGMENT))];

sw.addEventListener('install', (event) => {
	event.waitUntil(
		caches
			.open(APP_CACHE)
			.then((cache) => cache.addAll(PRECACHE))
			.then(() => sw.skipWaiting())
	);
});

sw.addEventListener('activate', (event) => {
	event.waitUntil(
		(async () => {
			for (const key of await caches.keys()) {
				// Drop previous app-shell builds and superseded Pyodide pins.
				if (key.startsWith('app-') && key !== APP_CACHE) await caches.delete(key);
				if (key.startsWith('pyodide-') && key !== PYODIDE_CACHE) await caches.delete(key);
				if (key.startsWith('wheels-') && key !== WHEELS_CACHE) await caches.delete(key);
			}
			await sw.clients.claim();
		})()
	);
});

sw.addEventListener('fetch', (event) => {
	const req = event.request;
	if (req.method !== 'GET') return;
	const url = new URL(req.url);

	// 1a. Pyodide CDN -> cache-first in its own pinned cache.
	if (url.origin === PYODIDE_ORIGIN && url.pathname.startsWith(PYODIDE_PATH)) {
		event.respondWith(
			(async () => {
				const cache = await caches.open(PYODIDE_CACHE);
				const hit = await cache.match(req);
				if (hit) return hit;
				const res = await fetch(req);
				if (res.ok) cache.put(req, res.clone());
				return res;
			})()
		);
		return;
	}

	// Only handle our own origin past this point.
	if (url.origin !== sw.location.origin) return;

	// 1a'. Self-hosted wheels -> cache-first, filled on first use. File names carry the
	// version, so a cache hit is always the right file.
	if (url.pathname.includes(WHEELS_SEGMENT) && url.pathname.endsWith('.whl')) {
		event.respondWith(
			caches.open(WHEELS_CACHE).then(async (cache) => {
				const hit = await cache.match(req);
				if (hit) return hit;
				const res = await fetch(req);
				if (res.ok) cache.put(req, res.clone());
				return res;
			})
		);
		return;
	}

	// 1b. Hashed build assets -> cache-first (immutable, hit is always correct).
	if (url.pathname.startsWith('/_app/immutable/')) {
		event.respondWith(
			caches.open(APP_CACHE).then(async (cache) => {
				const hit = await cache.match(req);
				if (hit) return hit;
				const res = await fetch(req);
				if (res.ok) cache.put(req, res.clone());
				return res;
			})
		);
		return;
	}

	// 1c. Navigations / prerendered HTML -> stale-while-revalidate.
	if (req.mode === 'navigate' || req.destination === 'document') {
		event.respondWith(
			caches.open(APP_CACHE).then(async (cache) => {
				const hit = await cache.match(req);
				const network = fetch(req)
					.then((res) => {
						if (res.ok) cache.put(req, res.clone());
						return res;
					})
					.catch(() => hit);
				return hit || network;
			})
		);
	}
});

export {};
