// Runs platform/static/gpubox/worker.js in a Node vm context that looks like a classic Web Worker
// (importScripts, self, postMessage; no require/module/window). Used by tests and the verifier, so the
// exact file the browser loads is the file that is checked.
import { createContext, runInContext } from 'node:vm';
import { readFileSync } from 'node:fs';
import { join, basename } from 'node:path';

const ROOT = join('platform', 'static', 'gpubox');

export function createWorkerVm() {
	const messages = [];
	const sandbox = { performance, URL, console, Float32Array, Int32Array, setTimeout, Math, JSON };
	sandbox.self = sandbox;
	sandbox.globalThis = sandbox;
	sandbox.location = { href: 'http://localhost/gpubox/worker.js' };
	sandbox.postMessage = (m) => messages.push(m);
	const ctx = createContext(sandbox);
	sandbox.importScripts = (...urls) => {
		for (const url of urls) {
			const file = join(ROOT, url.split('/').slice(-2, -1)[0], basename(url));
			runInContext(readFileSync(file, 'utf8'), ctx, { filename: file });
		}
	};
	runInContext(readFileSync(join(ROOT, 'worker.js'), 'utf8'), ctx, { filename: 'worker.js' });
	let id = 0;
	return {
		call(msg) {
			const mine = ++id;
			const before = messages.length;
			sandbox.onmessage({ data: { ...msg, id: mine } });
			const reply = messages.slice(before).find((m) => m.id === mine);
			if (!reply) throw new Error('worker sent no reply');
			return reply;
		}
	};
}
