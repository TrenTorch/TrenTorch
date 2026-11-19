import { createHash } from 'node:crypto';

/** Identifies the solution + harness a metrics.json was measured with, so stale metrics are caught. */
export function metricsKey(solution, harness) {
	return createHash('sha1')
		.update(solution)
		.update('\0')
		.update(harness)
		.digest('hex')
		.slice(0, 12);
}
