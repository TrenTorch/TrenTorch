"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AuthInvalidJwtError = exports.AuthWeakPasswordError = exports.AuthRefreshDiscardedError = exports.AuthRetryableFetchError = exports.AuthPKCECodeVerifierMissingError = exports.AuthPKCEGrantCodeExchangeError = exports.AuthImplicitGrantRedirectError = exports.AuthInvalidCredentialsError = exports.AuthInvalidTokenResponseError = exports.AuthSessionMissingError = exports.CustomAuthError = exports.AuthUnknownError = exports.AuthApiError = exports.AuthError = void 0;
exports.isAuthError = isAuthError;
exports.isAuthApiError = isAuthApiError;
exports.isAuthSessionMissingError = isAuthSessionMissingError;
exports.isAuthImplicitGrantRedirectError = isAuthImplicitGrantRedirectError;
exports.isAuthPKCECodeVerifierMissingError = isAuthPKCECodeVerifierMissingError;
exports.isAuthRetryableFetchError = isAuthRetryableFetchError;
exports.isAuthRefreshDiscardedError = isAuthRefreshDiscardedError;
exports.isAuthWeakPasswordError = isAuthWeakPasswordError;
/**
 * Base error thrown by Supabase Auth helpers.
 *
 * @example
 * ```ts
 * import { AuthError } from '@supabase/auth-js'
 *
 * throw new AuthError('Unexpected auth error', 500, 'unexpected')
 * ```
 */
class AuthError extends Error {
    constructor(message, status, code) {
        super(message);
        this.__isAuthError = true;
        this.name = 'AuthError';
        this.status = status;
        this.code = code;
    }
    toJSON() {
        return {
            name: this.name,
            message: this.message,
            status: this.status,
            code: this.code,
        };
    }
}
exports.AuthError = AuthError;
function isAuthError(error) {
    return typeof error === 'object' && error !== null && '__isAuthError' in error;
}
/**
 * Error returned directly from the GoTrue REST API.
 *
 * @example
 * ```ts
 * import { AuthApiError } from '@supabase/auth-js'
 *
 * throw new AuthApiError('Invalid credentials', 400, 'invalid_credentials')
 * ```
 */
class AuthApiError extends AuthError {
    constructor(message, status, code) {
        super(message, status, code);
        this.name = 'AuthApiError';
        this.status = status;
        this.code = code;
    }
}
exports.AuthApiError = AuthApiError;
function isAuthApiError(error) {
    return isAuthError(error) && error.name === 'AuthApiError';
}
/**
 * Wraps non-standard errors so callers can inspect the root cause.
 *
 * @example
 * ```ts
 * import { AuthUnknownError } from '@supabase/auth-js'
 *
 * try {
 *   await someAuthCall()
 * } catch (err) {
 *   throw new AuthUnknownError('Auth failed', err)
 * }
 * ```
 */
class AuthUnknownError extends AuthError {
    constructor(message, originalError) {
        super(message);
        this.name = 'AuthUnknownError';
        this.originalError = originalError;
    }
}
exports.AuthUnknownError = AuthUnknownError;
/**
 * Flexible error class used to create named auth errors at runtime.
 *
 * @example
 * ```ts
 * import { CustomAuthError } from '@supabase/auth-js'
 *
 * throw new CustomAuthError('My custom auth error', 'MyAuthError', 400, 'custom_code')
 * ```
 */
class CustomAuthError extends AuthError {
    constructor(message, name, status, code) {
        super(message, status, code);
        this.name = name;
        this.status = status;
    }
}
exports.CustomAuthError = CustomAuthError;
/**
 * Error thrown when an operation requires a session but none is present.
 *
 * @example
 * ```ts
 * import { AuthSessionMissingError } from '@supabase/auth-js'
 *
 * throw new AuthSessionMissingError()
 * ```
 */
class AuthSessionMissingError extends CustomAuthError {
    constructor() {
        super('Auth session missing!', 'AuthSessionMissingError', 400, undefined);
    }
}
exports.AuthSessionMissingError = AuthSessionMissingError;
function isAuthSessionMissingError(error) {
    return isAuthError(error) && error.name === 'AuthSessionMissingError';
}
/**
 * Error thrown when the token response is malformed.
 *
 * @example
 * ```ts
 * import { AuthInvalidTokenResponseError } from '@supabase/auth-js'
 *
 * throw new AuthInvalidTokenResponseError()
 * ```
 */
class AuthInvalidTokenResponseError extends CustomAuthError {
    constructor() {
        super('Auth session or user missing', 'AuthInvalidTokenResponseError', 500, undefined);
    }
}
exports.AuthInvalidTokenResponseError = AuthInvalidTokenResponseError;
/**
 * Error thrown when email/password credentials are invalid.
 *
 * @example
 * ```ts
 * import { AuthInvalidCredentialsError } from '@supabase/auth-js'
 *
 * throw new AuthInvalidCredentialsError('Email or password is incorrect')
 * ```
 */
class AuthInvalidCredentialsError extends CustomAuthError {
    constructor(message) {
        super(message, 'AuthInvalidCredentialsError', 400, undefined);
    }
}
exports.AuthInvalidCredentialsError = AuthInvalidCredentialsError;
/**
 * Error thrown when implicit grant redirects contain an error.
 *
 * @example
 * ```ts
 * import { AuthImplicitGrantRedirectError } from '@supabase/auth-js'
 *
 * throw new AuthImplicitGrantRedirectError('OAuth redirect failed', {
 *   error: 'access_denied',
 *   code: 'oauth_error',
 * })
 * ```
 */
class AuthImplicitGrantRedirectError extends CustomAuthError {
    constructor(message, details = null) {
        super(message, 'AuthImplicitGrantRedirectError', 500, undefined);
        this.details = null;
        this.details = details;
    }
    toJSON() {
        return Object.assign(Object.assign({}, super.toJSON()), { details: this.details });
    }
}
exports.AuthImplicitGrantRedirectError = AuthImplicitGrantRedirectError;
function isAuthImplicitGrantRedirectError(error) {
    return isAuthError(error) && error.name === 'AuthImplicitGrantRedirectError';
}
/**
 * Error thrown during PKCE code exchanges.
 *
 * @example
 * ```ts
 * import { AuthPKCEGrantCodeExchangeError } from '@supabase/auth-js'
 *
 * throw new AuthPKCEGrantCodeExchangeError('PKCE exchange failed')
 * ```
 */
class AuthPKCEGrantCodeExchangeError extends CustomAuthError {
    constructor(message, details = null) {
        super(message, 'AuthPKCEGrantCodeExchangeError', 500, undefined);
        this.details = null;
        this.details = details;
    }
    toJSON() {
        return Object.assign(Object.assign({}, super.toJSON()), { details: this.details });
    }
}
exports.AuthPKCEGrantCodeExchangeError = AuthPKCEGrantCodeExchangeError;
/**
 * Error thrown when the PKCE code verifier is not found in storage.
 * This typically happens when the auth flow was initiated in a different
 * browser, device, or the storage was cleared.
 *
 * @example
 * ```ts
 * import { AuthPKCECodeVerifierMissingError } from '@supabase/auth-js'
 *
 * throw new AuthPKCECodeVerifierMissingError()
 * ```
 */
class AuthPKCECodeVerifierMissingError extends CustomAuthError {
    constructor() {
        super('PKCE code verifier not found in storage. ' +
            'This can happen if the auth flow was initiated in a different browser or device, ' +
            'or if the storage was cleared. For SSR frameworks (Next.js, SvelteKit, etc.), ' +
            'use @supabase/ssr on both the server and client to store the code verifier in cookies.', 'AuthPKCECodeVerifierMissingError', 400, 'pkce_code_verifier_not_found');
    }
}
exports.AuthPKCECodeVerifierMissingError = AuthPKCECodeVerifierMissingError;
function isAuthPKCECodeVerifierMissingError(error) {
    return isAuthError(error) && error.name === 'AuthPKCECodeVerifierMissingError';
}
/**
 * Error thrown when a transient fetch issue occurs.
 *
 * @example
 * ```ts
 * import { AuthRetryableFetchError } from '@supabase/auth-js'
 *
 * throw new AuthRetryableFetchError('Service temporarily unavailable', 503)
 * ```
 */
class AuthRetryableFetchError extends CustomAuthError {
    constructor(message, status) {
        super(message, 'AuthRetryableFetchError', status, undefined);
    }
}
exports.AuthRetryableFetchError = AuthRetryableFetchError;
function isAuthRetryableFetchError(error) {
    return isAuthError(error) && error.name === 'AuthRetryableFetchError';
}
/**
 * Returned when the server rotated a refresh token successfully but the
 * client chose not to persist the rotated tokens because the local session
 * changed mid-flight. Usually means a concurrent `signOut` cleared storage
 * between when the refresh started and when it came back.
 *
 * Set on the `error` field of the refresh result so callers can tell "we
 * got rotated tokens but threw them away" apart from "the refresh failed."
 * The rotated session on the server will be picked up on the next refresh
 * via GoTrue's parent-of-active path.
 *
 * @example
 * ```ts
 * import { isAuthRefreshDiscardedError } from '@supabase/auth-js'
 *
 * if (isAuthRefreshDiscardedError(error)) {
 *   // Concurrent signOut/sign-in raced our refresh. Treat as a no-op.
 * }
 * ```
 */
class AuthRefreshDiscardedError extends CustomAuthError {
    constructor(message = 'Refresh result discarded: session state changed mid-flight (e.g., concurrent signOut)') {
        super(message, 'AuthRefreshDiscardedError', 409, undefined);
    }
}
exports.AuthRefreshDiscardedError = AuthRefreshDiscardedError;
function isAuthRefreshDiscardedError(error) {
    return isAuthError(error) && error.name === 'AuthRefreshDiscardedError';
}
/**
 * This error is thrown on certain methods when the password used is deemed
 * weak. Inspect the reasons to identify what password strength rules are
 * inadequate.
 */
/**
 * Error thrown when a supplied password is considered weak.
 *
 * @example
 * ```ts
 * import { AuthWeakPasswordError } from '@supabase/auth-js'
 *
 * throw new AuthWeakPasswordError('Password too short', 400, ['min_length'])
 * ```
 */
class AuthWeakPasswordError extends CustomAuthError {
    constructor(message, status, reasons) {
        super(message, 'AuthWeakPasswordError', status, 'weak_password');
        this.reasons = reasons;
    }
    toJSON() {
        return Object.assign(Object.assign({}, super.toJSON()), { reasons: this.reasons });
    }
}
exports.AuthWeakPasswordError = AuthWeakPasswordError;
function isAuthWeakPasswordError(error) {
    return isAuthError(error) && error.name === 'AuthWeakPasswordError';
}
/**
 * Error thrown when a JWT cannot be verified or parsed.
 *
 * @example
 * ```ts
 * import { AuthInvalidJwtError } from '@supabase/auth-js'
 *
 * throw new AuthInvalidJwtError('Token signature is invalid')
 * ```
 */
class AuthInvalidJwtError extends CustomAuthError {
    constructor(message) {
        super(message, 'AuthInvalidJwtError', 400, 'invalid_jwt');
    }
}
exports.AuthInvalidJwtError = AuthInvalidJwtError;
//# sourceMappingURL=errors.js.map