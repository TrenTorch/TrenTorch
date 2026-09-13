import { readFileSync } from 'node:fs';

export function readIfExists(path) {
	try {
		// Normalize to LF regardless of the authoring/checkout platform's line
		// endings -- a Windows checkout (CRLF) would otherwise bake literal
		// \r characters into every generated string, which is harmless for
		// Markdown but a real risk for Python source (mixed \r\n content
		// concatenated with \n content across questions, then exec'd).
		return readFileSync(path, 'utf-8').replace(/\r\n/g, '\n');
	} catch {
		return null;
	}
}
