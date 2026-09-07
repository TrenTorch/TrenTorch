/**
 * Register later cleanup task
 *
 * @param {() => void} onCleanup
 */
export function addCleanupTask(onCleanup: () => void): () => void;
/** Clean up all components and elements added to the document. */
export function cleanup(): void;
/**
 * Remove a cleanup task without running it.
 *
 * @param {() => void} onCleanup
 */
export function removeCleanupTask(onCleanup: () => void): void;
//# sourceMappingURL=cleanup.d.ts.map