import { JwtHeader, JwtPayload, SupportedStorage, User } from './types';
import { Uint8Array_ } from './webauthn.dom';
export declare function expiresAt(expiresIn: number): number;
/**
 * Generates a unique identifier for internal callback subscriptions.
 *
 * This function uses JavaScript Symbols to create guaranteed-unique identifiers
 * for auth state change callbacks. Symbols are ideal for this use case because:
 * - They are guaranteed unique by the JavaScript runtime
 * - They work in all environments (browser, SSR, Node.js)
 * - They avoid issues with Next.js 16 deterministic rendering requirements
 * - They are perfect for internal, non-serializable identifiers
 *
 * Note: This function is only used for internal subscription management,
 * not for security-critical operations like session tokens.
 */
export declare function generateCallbackId(): symbol;
export declare const isBrowser: () => boolean;
/**
 * Checks whether localStorage is supported on this browser.
 */
export declare const supportsLocalStorage: () => boolean;
/**
 * Extracts parameters encoded in the URL both in the query and fragment.
 */
export declare function parseParametersFromURL(href: string): {
    [parameter: string]: string;
};
type Fetch = typeof fetch;
export declare const resolveFetch: (customFetch?: Fetch) => Fetch;
export declare const looksLikeFetchResponse: (maybeResponse: unknown) => maybeResponse is Response;
export declare const setItemAsync: (storage: SupportedStorage, key: string, data: any) => Promise<void>;
export declare const getItemAsync: (storage: SupportedStorage, key: string) => Promise<unknown>;
export declare const removeItemAsync: (storage: SupportedStorage, key: string) => Promise<void>;
/**
 * A deferred represents some asynchronous work that is not yet finished, which
 * may or may not culminate in a value.
 * Taken from: https://github.com/mike-north/types/blob/master/src/async.ts
 */
export declare class Deferred<T = any> {
    static promiseConstructor: PromiseConstructor;
    readonly promise: PromiseLike<T>;
    readonly resolve: (value?: T | PromiseLike<T>) => void;
    readonly reject: (reason?: any) => any;
    constructor();
}
export declare function decodeJWT(token: string): {
    header: JwtHeader;
    payload: JwtPayload;
    signature: Uint8Array_;
    raw: {
        header: string;
        payload: string;
    };
};
/**
 * Creates a promise that resolves to null after some time.
 */
export declare function sleep(time: number): Promise<null>;
/**
 * Converts the provided async function into a retryable function. Each result
 * or thrown error is sent to the isRetryable function which should return true
 * if the function should run again.
 */
export declare function retryable<T>(fn: (attempt: number) => Promise<T>, isRetryable: (attempt: number, error: any | null, result?: T) => boolean): Promise<T>;
export declare function generatePKCEVerifier(): string;
export declare function generatePKCEChallenge(verifier: string): Promise<string>;
/**
 * Returns the flow id if it is a plausible flow id, `null` otherwise. Flow
 * ids can arrive via URL parameters, so anything outside the expected shape
 * is discarded before it is used to build a storage key.
 */
export declare function validatePKCEFlowId(flowId: unknown): string | null;
export declare function generatePKCEFlowId(): string;
export declare const pkceVerifierSlotKey: (storageKey: string, flowId: string) => string;
/**
 * The index is read-modify-write without a lock: two concurrent starts (e.g.
 * two tabs) can lose one index update. The losing flow still works — its slot
 * is addressed directly by key — but its entry is missing from the index, so
 * it escapes both ring eviction and removeAllPKCEVerifiers: the orphaned slot
 * persists for the storage medium's lifetime (up to the cookie max age in
 * cookie storage) and repeated races accumulate one orphan each. Accepted
 * trade-off: locking every flow start is far more intrusive than the leak.
 */
export declare function storePKCEVerifier(storage: SupportedStorage, storageKey: string, flowId: string, verifier: string, onEvictFlow?: (evictedFlowId: string) => void): Promise<void>;
/**
 * Looks up the verifier for `flowId`. When a flow id is given, only that slot
 * is consulted — deliberately no fallback to the fixed legacy key: submitting
 * another flow's verifier would burn the single-use auth code, and the
 * subsequent cleanup would delete a pending flow's only fallback. The legacy
 * key is read only when no flow id is available at all.
 */
export declare function retrievePKCEVerifier(storage: SupportedStorage, storageKey: string, flowId: string | null): Promise<{
    verifier: string | null;
    flowId: string | null;
}>;
/**
 * Removes a single flow's verifier. Never clears other flows' slots: with a
 * `flowId` only that slot is deleted (plus the legacy fixed key when it holds
 * the same verifier); without one, only the legacy fixed key is deleted.
 */
export declare function removePKCEVerifier(storage: SupportedStorage, storageKey: string, flowId: string | null): Promise<void>;
/**
 * Removes every pending verifier: all slots in the index, the index itself
 * and the fixed legacy key. Used on session teardown (sign-out, invalid
 * session) — matches the pre-slot behavior where tearing down the session
 * deleted the only verifier, and prevents long-lived stale verifier cookies.
 */
export declare function removeAllPKCEVerifiers(storage: SupportedStorage, storageKey: string): Promise<void>;
/**
 * Appends the reserved flow id parameter to a `redirectTo` URL, replacing any
 * existing occurrence. String-based (no URL round-trip) so custom schemes
 * (native deep links) and the exact encoding of the app's own parameters
 * survive untouched; an existing fragment stays at the end of the URL.
 */
export declare function appendFlowIdToRedirectTo(redirectTo: string, flowId: string): string;
export declare function getCodeChallengeAndMethod(storage: SupportedStorage, storageKey: string, isPasswordRecovery?: boolean, onEvictFlow?: (evictedFlowId: string) => void): Promise<[string, string, string]>;
export declare function parseResponseAPIVersion(response: Response): Date | null;
export declare function validateExp(exp: number): void;
export declare function getAlgorithm(alg: 'HS256' | 'RS256' | 'ES256' | (string & {})): RsaHashedImportParams | EcKeyImportParams;
export declare function validateUUID(str: string): void;
export declare function assertPasskeyExperimentalEnabled(experimental: {
    passkey?: boolean;
}): void;
export declare function assertRecoveryCodesExperimentalEnabled(experimental: {
    recoveryCodes?: boolean;
}): void;
export declare function userNotAvailableProxy(): User;
/**
 * Creates a proxy around a user object that warns when properties are accessed on the server.
 * This is used to alert developers that using user data from getSession() on the server is insecure.
 *
 * @param user The actual user object to wrap
 * @param suppressWarningRef An object with a 'value' property that controls warning suppression
 * @returns A proxied user object that warns on property access
 */
export declare function insecureUserWarningProxy(user: User, suppressWarningRef: {
    value: boolean;
}): User;
/**
 * Deep clones a JSON-serializable object using JSON.parse(JSON.stringify(obj)).
 * Note: Only works for JSON-safe data.
 */
export declare function deepClone<T>(obj: T): T;
export {};
//# sourceMappingURL=helpers.d.ts.map