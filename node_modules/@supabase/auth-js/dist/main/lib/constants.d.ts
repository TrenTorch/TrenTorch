/** Current session will be checked for refresh at this interval. */
export declare const AUTO_REFRESH_TICK_DURATION_MS: number;
/**
 * A token refresh will be attempted this many ticks before the current session expires. */
export declare const AUTO_REFRESH_TICK_THRESHOLD = 3;
export declare const EXPIRY_MARGIN_MS: number;
/**
 * After a refresh fails, serial callers (including the next auto-refresh
 * tick) within this window receive the cached failure instead of firing
 * another /token request. Two ticks: each outage burns at most one /token
 * call per cooldown window. Cleared on any successful refresh (locally or
 * via BroadcastChannel from another tab) and on `_removeSession`.
 */
export declare const REFRESH_FAILURE_COOLDOWN_MS: number;
export declare const GOTRUE_URL = "http://localhost:9999";
export declare const STORAGE_KEY = "supabase.auth.token";
export declare const AUDIENCE = "";
export declare const DEFAULT_HEADERS: {
    'X-Client-Info': string;
};
export declare const NETWORK_FAILURE: {
    MAX_RETRIES: number;
    RETRY_INTERVAL: number;
};
export declare const API_VERSION_HEADER_NAME = "X-Supabase-Api-Version";
export declare const API_VERSIONS: {
    '2024-01-01': {
        timestamp: number;
        name: string;
    };
};
export declare const BASE64URL_REGEX: RegExp;
/**
 * Reserved query parameter appended to `redirectTo` URLs (behind
 * `experimental.appendPkceFlowIdToRedirects`) that correlates a PKCE callback
 * with the code verifier stored when its flow started. It round-trips through
 * the auth server untouched and identifies a verifier slot in storage — the
 * verifier itself never appears in a URL.
 */
export declare const PKCE_FLOW_ID_PARAM = "sb_flow_id";
/**
 * Maximum number of PKCE code verifiers kept in storage at once. Starting a
 * new flow beyond this evicts the oldest pending verifier.
 */
export declare const PKCE_MAX_CONCURRENT_FLOWS = 5;
export declare const JWKS_TTL: number;
//# sourceMappingURL=constants.d.ts.map