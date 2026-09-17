import { statSync } from 'node:fs';

/** @param {string} path */
export function isDir(path) {
	try {
		return statSync(path).isDirectory();
	} catch {
		return false;
	}
}
