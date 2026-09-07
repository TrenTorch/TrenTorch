/**
 * Normalize the various shapes a channel error reason can take into a real `Error`.
 *
 * Transport-level channel errors arrive as a `CloseEvent`, a transport `Event`, an `Error`,
 * a string, or `undefined` depending on which path in the underlying socket fired. Server-reply
 * errors arrive as a payload object. This helper produces a consistent `Error` for every case
 * and preserves the original via `cause` so callers can still inspect the raw event.
 */
export declare function normalizeChannelError(reason: unknown): Error;
//# sourceMappingURL=normalizeChannelError.d.ts.map