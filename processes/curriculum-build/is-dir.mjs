import { statSync } from 'node:fs';

export function isDir(path) {
	try {
		return statSync(path).isDirectory();
	} catch {
		return false;
	}
}
