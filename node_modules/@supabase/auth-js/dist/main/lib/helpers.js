"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.pkceVerifierSlotKey = exports.Deferred = exports.removeItemAsync = exports.getItemAsync = exports.setItemAsync = exports.looksLikeFetchResponse = exports.resolveFetch = exports.supportsLocalStorage = exports.isBrowser = void 0;
exports.expiresAt = expiresAt;
exports.generateCallbackId = generateCallbackId;
exports.parseParametersFromURL = parseParametersFromURL;
exports.decodeJWT = decodeJWT;
exports.sleep = sleep;
exports.retryable = retryable;
exports.generatePKCEVerifier = generatePKCEVerifier;
exports.generatePKCEChallenge = generatePKCEChallenge;
exports.validatePKCEFlowId = validatePKCEFlowId;
exports.generatePKCEFlowId = generatePKCEFlowId;
exports.storePKCEVerifier = storePKCEVerifier;
exports.retrievePKCEVerifier = retrievePKCEVerifier;
exports.removePKCEVerifier = removePKCEVerifier;
exports.removeAllPKCEVerifiers = removeAllPKCEVerifiers;
exports.appendFlowIdToRedirectTo = appendFlowIdToRedirectTo;
exports.getCodeChallengeAndMethod = getCodeChallengeAndMethod;
exports.parseResponseAPIVersion = parseResponseAPIVersion;
exports.validateExp = validateExp;
exports.getAlgorithm = getAlgorithm;
exports.validateUUID = validateUUID;
exports.assertPasskeyExperimentalEnabled = assertPasskeyExperimentalEnabled;
exports.assertRecoveryCodesExperimentalEnabled = assertRecoveryCodesExperimentalEnabled;
exports.userNotAvailableProxy = userNotAvailableProxy;
exports.insecureUserWarningProxy = insecureUserWarningProxy;
exports.deepClone = deepClone;
const constants_1 = require("./constants");
const errors_1 = require("./errors");
const base64url_1 = require("./base64url");
function expiresAt(expiresIn) {
    const timeNow = Math.round(Date.now() / 1000);
    return timeNow + expiresIn;
}
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
function generateCallbackId() {
    return Symbol('auth-callback');
}
const isBrowser = () => typeof window !== 'undefined' && typeof document !== 'undefined';
exports.isBrowser = isBrowser;
const localStorageWriteTests = {
    tested: false,
    writable: false,
};
/**
 * Checks whether localStorage is supported on this browser.
 */
const supportsLocalStorage = () => {
    if (!(0, exports.isBrowser)()) {
        return false;
    }
    try {
        if (typeof globalThis.localStorage !== 'object') {
            return false;
        }
    }
    catch (e) {
        // DOM exception when accessing `localStorage`
        return false;
    }
    if (localStorageWriteTests.tested) {
        return localStorageWriteTests.writable;
    }
    const randomKey = `lswt-${Math.random()}${Math.random()}`;
    try {
        globalThis.localStorage.setItem(randomKey, randomKey);
        globalThis.localStorage.removeItem(randomKey);
        localStorageWriteTests.tested = true;
        localStorageWriteTests.writable = true;
    }
    catch (e) {
        // localStorage can't be written to
        // https://www.chromium.org/for-testers/bug-reporting-guidelines/uncaught-securityerror-failed-to-read-the-localstorage-property-from-window-access-is-denied-for-this-document
        localStorageWriteTests.tested = true;
        localStorageWriteTests.writable = false;
    }
    return localStorageWriteTests.writable;
};
exports.supportsLocalStorage = supportsLocalStorage;
/**
 * Extracts parameters encoded in the URL both in the query and fragment.
 */
function parseParametersFromURL(href) {
    const result = {};
    const url = new URL(href);
    if (url.hash && url.hash[0] === '#') {
        try {
            const hashSearchParams = new URLSearchParams(url.hash.substring(1));
            hashSearchParams.forEach((value, key) => {
                result[key] = value;
            });
        }
        catch (_e) {
            // hash is not a query string
        }
    }
    // search parameters take precedence over hash parameters
    url.searchParams.forEach((value, key) => {
        result[key] = value;
    });
    return result;
}
const resolveFetch = (customFetch) => {
    if (customFetch) {
        return (...args) => customFetch(...args);
    }
    return (...args) => fetch(...args);
};
exports.resolveFetch = resolveFetch;
const looksLikeFetchResponse = (maybeResponse) => {
    return (typeof maybeResponse === 'object' &&
        maybeResponse !== null &&
        'status' in maybeResponse &&
        'ok' in maybeResponse &&
        'json' in maybeResponse &&
        typeof maybeResponse.json === 'function');
};
exports.looksLikeFetchResponse = looksLikeFetchResponse;
// Storage helpers
const setItemAsync = async (storage, key, data) => {
    await storage.setItem(key, JSON.stringify(data));
};
exports.setItemAsync = setItemAsync;
const getItemAsync = async (storage, key) => {
    const value = await storage.getItem(key);
    if (!value) {
        return null;
    }
    try {
        return JSON.parse(value);
    }
    catch (_a) {
        // Storage values are always written as JSON via setItemAsync. A non-JSON
        // value means the entry is corrupted (e.g. mismatched chunked cookies in
        // SSR contexts). Treat as absent so callers do not mutate or re-save the
        // garbage, which would otherwise trigger a TypeError downstream and
        // leak the raw value into error logs.
        return null;
    }
};
exports.getItemAsync = getItemAsync;
const removeItemAsync = async (storage, key) => {
    await storage.removeItem(key);
};
exports.removeItemAsync = removeItemAsync;
/**
 * A deferred represents some asynchronous work that is not yet finished, which
 * may or may not culminate in a value.
 * Taken from: https://github.com/mike-north/types/blob/master/src/async.ts
 */
class Deferred {
    constructor() {
        // eslint-disable-next-line @typescript-eslint/no-extra-semi
        ;
        this.promise = new Deferred.promiseConstructor((res, rej) => {
            // eslint-disable-next-line @typescript-eslint/no-extra-semi
            ;
            this.resolve = res;
            this.reject = rej;
        });
    }
}
exports.Deferred = Deferred;
Deferred.promiseConstructor = Promise;
function decodeJWT(token) {
    const parts = token.split('.');
    if (parts.length !== 3) {
        throw new errors_1.AuthInvalidJwtError('Invalid JWT structure');
    }
    // Regex checks for base64url format
    for (let i = 0; i < parts.length; i++) {
        if (!constants_1.BASE64URL_REGEX.test(parts[i])) {
            throw new errors_1.AuthInvalidJwtError('JWT not in base64url format');
        }
    }
    const data = {
        // using base64url lib
        header: JSON.parse((0, base64url_1.stringFromBase64URL)(parts[0])),
        payload: JSON.parse((0, base64url_1.stringFromBase64URL)(parts[1])),
        signature: (0, base64url_1.base64UrlToUint8Array)(parts[2]),
        raw: {
            header: parts[0],
            payload: parts[1],
        },
    };
    return data;
}
/**
 * Creates a promise that resolves to null after some time.
 */
async function sleep(time) {
    return await new Promise((accept) => {
        setTimeout(() => accept(null), time);
    });
}
/**
 * Converts the provided async function into a retryable function. Each result
 * or thrown error is sent to the isRetryable function which should return true
 * if the function should run again.
 */
function retryable(fn, isRetryable) {
    const promise = new Promise((accept, reject) => {
        // eslint-disable-next-line @typescript-eslint/no-extra-semi
        ;
        (async () => {
            for (let attempt = 0; attempt < Infinity; attempt++) {
                try {
                    const result = await fn(attempt);
                    if (!isRetryable(attempt, null, result)) {
                        accept(result);
                        return;
                    }
                }
                catch (e) {
                    if (!isRetryable(attempt, e)) {
                        reject(e);
                        return;
                    }
                }
            }
        })();
    });
    return promise;
}
function dec2hex(dec) {
    return ('0' + dec.toString(16)).substr(-2);
}
// Functions below taken from: https://stackoverflow.com/questions/63309409/creating-a-code-verifier-and-challenge-for-pkce-auth-on-spotify-api-in-reactjs
function generatePKCEVerifier() {
    const verifierLength = 56;
    const array = new Uint32Array(verifierLength);
    if (typeof crypto === 'undefined') {
        const charSet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';
        const charSetLen = charSet.length;
        let verifier = '';
        for (let i = 0; i < verifierLength; i++) {
            verifier += charSet.charAt(Math.floor(Math.random() * charSetLen));
        }
        return verifier;
    }
    crypto.getRandomValues(array);
    return Array.from(array, dec2hex).join('');
}
async function sha256(randomString) {
    const encoder = new TextEncoder();
    const encodedData = encoder.encode(randomString);
    const hash = await crypto.subtle.digest('SHA-256', encodedData);
    const bytes = new Uint8Array(hash);
    return Array.from(bytes)
        .map((c) => String.fromCharCode(c))
        .join('');
}
async function generatePKCEChallenge(verifier) {
    const hasCryptoSupport = typeof crypto !== 'undefined' &&
        typeof crypto.subtle !== 'undefined' &&
        typeof TextEncoder !== 'undefined';
    if (!hasCryptoSupport) {
        console.warn('WebCrypto API is not supported. Code challenge method will default to use plain instead of sha256.');
        return verifier;
    }
    const hashed = await sha256(verifier);
    return btoa(hashed).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
const PKCE_FLOW_ID_PATTERN = /^[a-zA-Z0-9_-]{8,64}$/;
/**
 * Returns the flow id if it is a plausible flow id, `null` otherwise. Flow
 * ids can arrive via URL parameters, so anything outside the expected shape
 * is discarded before it is used to build a storage key.
 */
function validatePKCEFlowId(flowId) {
    return typeof flowId === 'string' && PKCE_FLOW_ID_PATTERN.test(flowId) ? flowId : null;
}
function generatePKCEFlowId() {
    if (typeof crypto !== 'undefined' && typeof crypto.getRandomValues === 'function') {
        const bytes = new Uint8Array(16);
        crypto.getRandomValues(bytes);
        return Array.from(bytes, dec2hex).join('');
    }
    let flowId = '';
    for (let i = 0; i < 32; i++) {
        flowId += Math.floor(Math.random() * 16).toString(16);
    }
    return flowId;
}
// Slot keys deliberately end in `-code-verifier`: @supabase/ssr's server
// cookie adapter only persists writes immediately for keys with that suffix
// (no auth event fires when a verifier is stored). They also contain no dot,
// because @supabase/ssr chunks oversized cookies as `<key>.<number>` and a
// dot-delimited key could be mistaken for a chunk of the fixed
// `-code-verifier` cookie and clobbered by its chunk management.
const pkceVerifierSlotKey = (storageKey, flowId) => `${storageKey}-flow-${flowId}-code-verifier`;
exports.pkceVerifierSlotKey = pkceVerifierSlotKey;
const pkceFlowIndexKey = (storageKey) => `${storageKey}-flows-code-verifier`;
/**
 * Storage adapters cannot enumerate keys, so the ids of pending verifier
 * slots are tracked in an index entry, oldest first. Index entries pass
 * through the same validation as URL-provided flow ids: with cookie-based
 * storage the index contents are no more trustworthy than a URL parameter.
 */
async function getPKCEFlowIndex(storage, storageKey) {
    const index = await (0, exports.getItemAsync)(storage, pkceFlowIndexKey(storageKey));
    return Array.isArray(index)
        ? index.filter((id) => validatePKCEFlowId(id) !== null)
        : [];
}
/**
 * The index is read-modify-write without a lock: two concurrent starts (e.g.
 * two tabs) can lose one index update. The losing flow still works — its slot
 * is addressed directly by key — but its entry is missing from the index, so
 * it escapes both ring eviction and removeAllPKCEVerifiers: the orphaned slot
 * persists for the storage medium's lifetime (up to the cookie max age in
 * cookie storage) and repeated races accumulate one orphan each. Accepted
 * trade-off: locking every flow start is far more intrusive than the leak.
 */
async function storePKCEVerifier(storage, storageKey, flowId, verifier, onEvictFlow) {
    await (0, exports.setItemAsync)(storage, (0, exports.pkceVerifierSlotKey)(storageKey, flowId), verifier);
    const index = (await getPKCEFlowIndex(storage, storageKey)).filter((id) => id !== flowId);
    index.push(flowId);
    while (index.length > constants_1.PKCE_MAX_CONCURRENT_FLOWS) {
        const evicted = index.shift();
        await (0, exports.removeItemAsync)(storage, (0, exports.pkceVerifierSlotKey)(storageKey, evicted));
        onEvictFlow === null || onEvictFlow === void 0 ? void 0 : onEvictFlow(evicted);
    }
    await (0, exports.setItemAsync)(storage, pkceFlowIndexKey(storageKey), index);
    // Deprecation-window dual write: exchanges that cannot identify their flow
    // (older SDK versions, redirects without the flow id parameter) read the
    // fixed key, which mirrors the most recently started flow.
    await (0, exports.setItemAsync)(storage, `${storageKey}-code-verifier`, verifier);
}
/**
 * Looks up the verifier for `flowId`. When a flow id is given, only that slot
 * is consulted — deliberately no fallback to the fixed legacy key: submitting
 * another flow's verifier would burn the single-use auth code, and the
 * subsequent cleanup would delete a pending flow's only fallback. The legacy
 * key is read only when no flow id is available at all.
 */
async function retrievePKCEVerifier(storage, storageKey, flowId) {
    if (flowId) {
        const verifier = await (0, exports.getItemAsync)(storage, (0, exports.pkceVerifierSlotKey)(storageKey, flowId));
        return { verifier: typeof verifier === 'string' ? verifier : null, flowId };
    }
    const verifier = await (0, exports.getItemAsync)(storage, `${storageKey}-code-verifier`);
    return { verifier: typeof verifier === 'string' ? verifier : null, flowId: null };
}
/**
 * Removes a single flow's verifier. Never clears other flows' slots: with a
 * `flowId` only that slot is deleted (plus the legacy fixed key when it holds
 * the same verifier); without one, only the legacy fixed key is deleted.
 */
async function removePKCEVerifier(storage, storageKey, flowId) {
    const legacyKey = `${storageKey}-code-verifier`;
    if (!flowId) {
        await (0, exports.removeItemAsync)(storage, legacyKey);
        return;
    }
    const slotKey = (0, exports.pkceVerifierSlotKey)(storageKey, flowId);
    const slotValue = await (0, exports.getItemAsync)(storage, slotKey);
    await (0, exports.removeItemAsync)(storage, slotKey);
    // Skip the index rewrite when the flow was never indexed (e.g. a failed
    // exchange for an absent slot): on cookie storage every write is a full
    // Set-Cookie cycle.
    const index = await getPKCEFlowIndex(storage, storageKey);
    const remaining = index.filter((id) => id !== flowId);
    if (remaining.length !== index.length) {
        if (remaining.length > 0) {
            await (0, exports.setItemAsync)(storage, pkceFlowIndexKey(storageKey), remaining);
        }
        else {
            await (0, exports.removeItemAsync)(storage, pkceFlowIndexKey(storageKey));
        }
    }
    if (slotValue != null && slotValue === (await (0, exports.getItemAsync)(storage, legacyKey))) {
        await (0, exports.removeItemAsync)(storage, legacyKey);
    }
}
/**
 * Removes every pending verifier: all slots in the index, the index itself
 * and the fixed legacy key. Used on session teardown (sign-out, invalid
 * session) — matches the pre-slot behavior where tearing down the session
 * deleted the only verifier, and prevents long-lived stale verifier cookies.
 */
async function removeAllPKCEVerifiers(storage, storageKey) {
    const index = await getPKCEFlowIndex(storage, storageKey);
    for (const flowId of index) {
        await (0, exports.removeItemAsync)(storage, (0, exports.pkceVerifierSlotKey)(storageKey, flowId));
    }
    await (0, exports.removeItemAsync)(storage, pkceFlowIndexKey(storageKey));
    await (0, exports.removeItemAsync)(storage, `${storageKey}-code-verifier`);
}
/**
 * Appends the reserved flow id parameter to a `redirectTo` URL, replacing any
 * existing occurrence. String-based (no URL round-trip) so custom schemes
 * (native deep links) and the exact encoding of the app's own parameters
 * survive untouched; an existing fragment stays at the end of the URL.
 */
function appendFlowIdToRedirectTo(redirectTo, flowId) {
    const hashIndex = redirectTo.indexOf('#');
    let base = hashIndex === -1 ? redirectTo : redirectTo.slice(0, hashIndex);
    const fragment = hashIndex === -1 ? '' : redirectTo.slice(hashIndex);
    const queryIndex = base.indexOf('?');
    if (queryIndex !== -1) {
        const path = base.slice(0, queryIndex);
        const remaining = base
            .slice(queryIndex + 1)
            .split('&')
            .filter((pair) => pair !== '' && pair !== constants_1.PKCE_FLOW_ID_PARAM && !pair.startsWith(`${constants_1.PKCE_FLOW_ID_PARAM}=`));
        base = remaining.length > 0 ? `${path}?${remaining.join('&')}` : path;
    }
    const separator = base.includes('?') ? '&' : '?';
    return `${base}${separator}${constants_1.PKCE_FLOW_ID_PARAM}=${encodeURIComponent(flowId)}${fragment}`;
}
async function getCodeChallengeAndMethod(storage, storageKey, isPasswordRecovery = false, onEvictFlow) {
    const codeVerifier = generatePKCEVerifier();
    let storedCodeVerifier = codeVerifier;
    if (isPasswordRecovery) {
        storedCodeVerifier += '/recovery';
    }
    const flowId = generatePKCEFlowId();
    await storePKCEVerifier(storage, storageKey, flowId, storedCodeVerifier, onEvictFlow);
    const codeChallenge = await generatePKCEChallenge(codeVerifier);
    const codeChallengeMethod = codeVerifier === codeChallenge ? 'plain' : 's256';
    return [codeChallenge, codeChallengeMethod, flowId];
}
/** Parses the API version which is 2YYY-MM-DD. */
const API_VERSION_REGEX = /^2[0-9]{3}-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$/i;
function parseResponseAPIVersion(response) {
    const apiVersion = response.headers.get(constants_1.API_VERSION_HEADER_NAME);
    if (!apiVersion) {
        return null;
    }
    if (!apiVersion.match(API_VERSION_REGEX)) {
        return null;
    }
    try {
        const date = new Date(`${apiVersion}T00:00:00.0Z`);
        return date;
    }
    catch (_e) {
        return null;
    }
}
function validateExp(exp) {
    if (!exp) {
        throw new Error('Missing exp claim');
    }
    const timeNow = Math.floor(Date.now() / 1000);
    if (exp <= timeNow) {
        throw new Error('JWT has expired');
    }
}
function getAlgorithm(alg) {
    switch (alg) {
        case 'RS256':
            return {
                name: 'RSASSA-PKCS1-v1_5',
                hash: { name: 'SHA-256' },
            };
        case 'ES256':
            return {
                name: 'ECDSA',
                namedCurve: 'P-256',
                hash: { name: 'SHA-256' },
            };
        default:
            throw new Error('Invalid alg claim');
    }
}
const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
function validateUUID(str) {
    if (!UUID_REGEX.test(str)) {
        throw new Error('@supabase/auth-js: Expected parameter to be UUID but is not');
    }
}
function assertPasskeyExperimentalEnabled(experimental) {
    if (!experimental.passkey) {
        throw new Error('@supabase/auth-js: the passkey API is experimental and disabled by default. Enable it by passing `auth: { experimental: { passkey: true } }` to createClient (or to the GoTrueClient constructor).');
    }
}
function assertRecoveryCodesExperimentalEnabled(experimental) {
    if (!experimental.recoveryCodes) {
        throw new Error('@supabase/auth-js: the MFA recovery codes API is experimental and disabled by default. Enable it by passing `auth: { experimental: { recoveryCodes: true } }` to createClient (or to the GoTrueClient constructor).');
    }
}
function userNotAvailableProxy() {
    const proxyTarget = {};
    return new Proxy(proxyTarget, {
        get: (target, prop) => {
            if (prop === '__isUserNotAvailableProxy') {
                return true;
            }
            // Preventative check for common problematic symbols during cloning/inspection
            // These symbols might be accessed by structuredClone or other internal mechanisms.
            if (typeof prop === 'symbol') {
                const sProp = prop.toString();
                if (sProp === 'Symbol(Symbol.toPrimitive)' ||
                    sProp === 'Symbol(Symbol.toStringTag)' ||
                    sProp === 'Symbol(util.inspect.custom)') {
                    // Node.js util.inspect
                    return undefined;
                }
            }
            throw new Error(`@supabase/auth-js: client was created with userStorage option and there was no user stored in the user storage. Accessing the "${prop}" property of the session object is not supported. Please use getUser() instead.`);
        },
        set: (_target, prop) => {
            throw new Error(`@supabase/auth-js: client was created with userStorage option and there was no user stored in the user storage. Setting the "${prop}" property of the session object is not supported. Please use getUser() to fetch a user object you can manipulate.`);
        },
        deleteProperty: (_target, prop) => {
            throw new Error(`@supabase/auth-js: client was created with userStorage option and there was no user stored in the user storage. Deleting the "${prop}" property of the session object is not supported. Please use getUser() to fetch a user object you can manipulate.`);
        },
    });
}
/**
 * Creates a proxy around a user object that warns when properties are accessed on the server.
 * This is used to alert developers that using user data from getSession() on the server is insecure.
 *
 * @param user The actual user object to wrap
 * @param suppressWarningRef An object with a 'value' property that controls warning suppression
 * @returns A proxied user object that warns on property access
 */
function insecureUserWarningProxy(user, suppressWarningRef) {
    return new Proxy(user, {
        get: (target, prop, receiver) => {
            // Allow internal checks without warning
            if (prop === '__isInsecureUserWarningProxy') {
                return true;
            }
            // Preventative check for common problematic symbols during cloning/inspection
            // These symbols might be accessed by structuredClone or other internal mechanisms
            if (typeof prop === 'symbol') {
                const sProp = prop.toString();
                if (sProp === 'Symbol(Symbol.toPrimitive)' ||
                    sProp === 'Symbol(Symbol.toStringTag)' ||
                    sProp === 'Symbol(util.inspect.custom)' ||
                    sProp === 'Symbol(nodejs.util.inspect.custom)') {
                    // Return the actual value for these symbols to allow proper inspection
                    return Reflect.get(target, prop, receiver);
                }
            }
            // Emit warning on first property access
            if (!suppressWarningRef.value && typeof prop === 'string') {
                console.warn('Using the user object as returned from supabase.auth.getSession() or from some supabase.auth.onAuthStateChange() events could be insecure! This value comes directly from the storage medium (usually cookies on the server) and may not be authentic. Use supabase.auth.getUser() instead which authenticates the data by contacting the Supabase Auth server.');
                suppressWarningRef.value = true;
            }
            return Reflect.get(target, prop, receiver);
        },
    });
}
/**
 * Deep clones a JSON-serializable object using JSON.parse(JSON.stringify(obj)).
 * Note: Only works for JSON-safe data.
 */
function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}
//# sourceMappingURL=helpers.js.map