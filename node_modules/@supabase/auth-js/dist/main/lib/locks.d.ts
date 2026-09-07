/**
 * Lock primitives retained for backwards-compatible imports. The auth client
 * coordinates refreshes itself (deduping in-instance callers onto a shared
 * in-flight promise) and lets the GoTrue server resolve cross-instance races,
 * so it does not invoke any primitive from this module. The functions still
 * work for direct callers that need a navigator.locks-backed or in-process
 * exclusive lock of their own.
 */
/**
 * @deprecated Debug flag for `navigatorLock` / `processLock`. The auth
 * client ignores both, so this has no client-side effect.
 * @experimental
 */
export declare const internals: {
    /**
     * @experimental
     */
    debug: boolean;
};
/**
 * An error thrown when a lock cannot be acquired after some amount of time.
 *
 * @deprecated The auth client doesn't acquire locks around auth operations,
 * so this error never originates from `supabase.auth.*` calls. Direct callers
 * of `navigatorLock` / `processLock` still receive it on acquire timeout.
 */
export declare abstract class LockAcquireTimeoutError extends Error {
    readonly isAcquireTimeout = true;
    constructor(message: string);
}
/**
 * @deprecated The auth client doesn't call `navigator.locks`, so this error
 * never originates from `supabase.auth.*` calls. Direct callers of
 * `navigatorLock` still receive it on acquire timeout.
 */
export declare class NavigatorLockAcquireTimeoutError extends LockAcquireTimeoutError {
}
/**
 * @deprecated The auth client doesn't run `processLock`, so this error
 * never originates from `supabase.auth.*` calls. Direct callers of
 * `processLock` still receive it on acquire timeout.
 */
export declare class ProcessLockAcquireTimeoutError extends LockAcquireTimeoutError {
}
/**
 * Implements a global exclusive lock using the Navigator LockManager API. It
 * is available on all browsers released after 2022-03-15 with Safari being the
 * last one to release support. If the API is not available, this function will
 * throw. Make sure you check availablility before configuring {@link
 * GoTrueClient}.
 *
 * You can turn on debugging by setting the `supabase.gotrue-js.locks.debug`
 * local storage item to `true`.
 *
 * Internals:
 *
 * Since the LockManager API does not preserve stack traces for the async
 * function passed in the `request` method, a trick is used where acquiring the
 * lock releases a previously started promise to run the operation in the `fn`
 * function. The lock waits for that promise to finish (with or without error),
 * while the function will finally wait for the result anyway.
 *
 * @param name Name of the lock to be acquired.
 * @param acquireTimeout If negative, no timeout. If 0 an error is thrown if
 *                       the lock can't be acquired without waiting. If positive, the lock acquire
 *                       will time out after so many milliseconds. An error is
 *                       a timeout if it has `isAcquireTimeout` set to true.
 * @param fn The operation to run once the lock is acquired.
 *
 * @deprecated The auth client coordinates refreshes itself and the server
 * resolves concurrent refresh races, so passing `{ lock: navigatorLock }`
 * to it has no effect. You can safely drop the import from your client setup.
 */
export declare function navigatorLock<R>(name: string, acquireTimeout: number, fn: () => Promise<R>): Promise<R>;
/**
 * Implements a global exclusive lock that works only in the current process.
 * Useful for environments like React Native or other non-browser
 * single-process (i.e. no concept of "tabs") environments.
 *
 * Use {@link navigatorLock} in browser environments.
 *
 * @param name Name of the lock to be acquired.
 * @param acquireTimeout If negative, no timeout. If 0 an error is thrown if
 *                       the lock can't be acquired without waiting. If positive, the lock acquire
 *                       will time out after so many milliseconds. An error is
 *                       a timeout if it has `isAcquireTimeout` set to true.
 * @param fn The operation to run once the lock is acquired.
 *
 * @deprecated The auth client coordinates refreshes itself and the server
 * resolves concurrent refresh races, so passing `{ lock: processLock }`
 * to it has no effect. You can safely drop the import from your client setup.
 *
 * @example
 * ```ts
 * await processLock('migrate', 5000, async () => {
 *   await runMigration()
 * })
 * ```
 */
export declare function processLock<R>(name: string, acquireTimeout: number, fn: () => Promise<R>): Promise<R>;
//# sourceMappingURL=locks.d.ts.map