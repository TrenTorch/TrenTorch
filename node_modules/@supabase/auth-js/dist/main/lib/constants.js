"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.JWKS_TTL = exports.PKCE_MAX_CONCURRENT_FLOWS = exports.PKCE_FLOW_ID_PARAM = exports.BASE64URL_REGEX = exports.API_VERSIONS = exports.API_VERSION_HEADER_NAME = exports.NETWORK_FAILURE = exports.DEFAULT_HEADERS = exports.AUDIENCE = exports.STORAGE_KEY = exports.GOTRUE_URL = exports.REFRESH_FAILURE_COOLDOWN_MS = exports.EXPIRY_MARGIN_MS = exports.AUTO_REFRESH_TICK_THRESHOLD = exports.AUTO_REFRESH_TICK_DURATION_MS = void 0;
const version_1 = require("./version");
/** Current session will be checked for refresh at this interval. */
exports.AUTO_REFRESH_TICK_DURATION_MS = 30 * 1000;
/**
 * A token refresh will be attempted this many ticks before the current session expires. */
exports.AUTO_REFRESH_TICK_THRESHOLD = 3;
/*
 * Earliest time before an access token expires that the session should be refreshed.
 */
exports.EXPIRY_MARGIN_MS = exports.AUTO_REFRESH_TICK_THRESHOLD * exports.AUTO_REFRESH_TICK_DURATION_MS;
/**
 * After a refresh fails, serial callers (including the next auto-refresh
 * tick) within this window receive the cached failure instead of firing
 * another /token request. Two ticks: each outage burns at most one /token
 * call per cooldown window. Cleared on any successful refresh (locally or
 * via BroadcastChannel from another tab) and on `_removeSession`.
 */
exports.REFRESH_FAILURE_COOLDOWN_MS = 2 * exports.AUTO_REFRESH_TICK_DURATION_MS;
exports.GOTRUE_URL = 'http://localhost:9999';
exports.STORAGE_KEY = 'supabase.auth.token';
exports.AUDIENCE = '';
exports.DEFAULT_HEADERS = { 'X-Client-Info': `gotrue-js/${version_1.version}` };
exports.NETWORK_FAILURE = {
    MAX_RETRIES: 10,
    RETRY_INTERVAL: 2, // in deciseconds
};
exports.API_VERSION_HEADER_NAME = 'X-Supabase-Api-Version';
exports.API_VERSIONS = {
    '2024-01-01': {
        timestamp: Date.parse('2024-01-01T00:00:00.0Z'),
        name: '2024-01-01',
    },
};
exports.BASE64URL_REGEX = /^([a-z0-9_-]{4})*($|[a-z0-9_-]{3}$|[a-z0-9_-]{2}$)$/i;
/**
 * Reserved query parameter appended to `redirectTo` URLs (behind
 * `experimental.appendPkceFlowIdToRedirects`) that correlates a PKCE callback
 * with the code verifier stored when its flow started. It round-trips through
 * the auth server untouched and identifies a verifier slot in storage — the
 * verifier itself never appears in a URL.
 */
exports.PKCE_FLOW_ID_PARAM = 'sb_flow_id';
/**
 * Maximum number of PKCE code verifiers kept in storage at once. Starting a
 * new flow beyond this evicts the oldest pending verifier.
 */
exports.PKCE_MAX_CONCURRENT_FLOWS = 5;
exports.JWKS_TTL = 10 * 60 * 1000; // 10 minutes
//# sourceMappingURL=constants.js.map