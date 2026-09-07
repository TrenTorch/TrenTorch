import GoTrueAdminApi from './GoTrueAdminApi';
import { AuthError } from './lib/errors';
import { Fetch } from './lib/fetch';
import { Deferred } from './lib/helpers';
import type { AuthChangeEvent, AuthFlowType, AuthOtpResponse, AuthResponse, AuthTokenResponse, AuthTokenResponsePassword, CallRefreshTokenResult, GoTrueClientOptions, GoTrueMFAApi, InitializeResult, JWK, JwtHeader, JwtPayload, LockFunc, OAuthResponse, AuthOAuthServerApi, ResendParams, Session, SignInAnonymouslyCredentials, SignInWithIdTokenCredentials, SignInWithOAuthCredentials, SignInWithPasswordCredentials, SignInWithPasswordlessCredentials, SignInWithSSO, SignOut, SignUpWithPasswordCredentials, SSOResponse, Subscription, SupportedStorage, User, UserAttributes, UserIdentity, UserResponse, VerifyOtpParams, Web3Credentials, AuthPasskeyApi, ExperimentalFeatureFlags, SignInWithPasskeyCredentials, RegisterPasskeyCredentials, AuthPasskeyRegistrationVerifyResponse, AuthPasskeyAuthenticationVerifyResponse } from './lib/types';
export default class GoTrueClient {
    private static nextInstanceID;
    private instanceID;
    /**
     * Namespace for the GoTrue admin methods.
     * These methods should only be used in a trusted server-side environment.
     */
    admin: GoTrueAdminApi;
    /**
     * Namespace for the MFA methods.
     */
    mfa: GoTrueMFAApi;
    /**
     * Namespace for the OAuth 2.1 authorization server methods.
     * Only relevant when the OAuth 2.1 server is enabled in Supabase Auth.
     * Used to implement the authorization code flow on the consent page.
     */
    oauth: AuthOAuthServerApi;
    /**
     * Namespace for passkey methods.
     * Includes lower-level two-step registration/authentication and passkey management.
     *
     * Requires `auth.experimental.passkey: true`; otherwise all methods throw.
     */
    passkey: AuthPasskeyApi;
    /**
     * The storage key used to identify the values saved in localStorage
     */
    protected storageKey: string;
    protected flowType: AuthFlowType;
    /**
     * The JWKS used for verifying asymmetric JWTs
     */
    protected get jwks(): {
        keys: JWK[];
    };
    protected set jwks(value: {
        keys: JWK[];
    });
    protected get jwks_cached_at(): number;
    protected set jwks_cached_at(value: number);
    protected autoRefreshToken: boolean;
    protected persistSession: boolean;
    protected storage: SupportedStorage;
    /**
     * @experimental
     */
    protected userStorage: SupportedStorage | null;
    protected memoryStorage: {
        [key: string]: string;
    } | null;
    protected stateChangeEmitters: Map<string | symbol, Subscription>;
    protected autoRefreshTicker: ReturnType<typeof setInterval> | null;
    protected autoRefreshTickTimeout: ReturnType<typeof setTimeout> | null;
    protected visibilityChangedCallback: (() => Promise<any>) | null;
    protected refreshingDeferred: Deferred<CallRefreshTokenResult> | null;
    /**
     * Cache of the most recent refresh failure, keyed by the refresh token
     * that failed. Serial callers passing the *same* token within
     * `REFRESH_FAILURE_COOLDOWN_MS` (including subsequent auto-refresh ticks)
     * receive this cached result instead of firing another `/token` request.
     * Callers passing a *different* token (token rotation pickup, explicit
     * `setSession`/`refreshSession({ refresh_token })`, multi-account switch)
     * bypass the cache and attempt a fresh refresh as they should.
     * Cleared on any successful refresh (locally or via BroadcastChannel from
     * another tab) and on `_removeSession`.
     *
     * Pairs with `refreshingDeferred`: concurrent callers share the in-flight
     * promise, serial callers within the cooldown share the failure result.
     */
    protected lastRefreshFailure: {
        refreshToken: string;
        result: CallRefreshTokenResult;
        expiresAt: number;
    } | null;
    /**
     * Monotonic counter incremented at the top of `_removeSession`, before any
     * `await`. The commit guard inside `_callRefreshToken` captures this value
     * before `_saveSession` and re-checks it after, so a `signOut` that
     * interleaves inside `_saveSession`'s storage-write awaits is still caught
     * (the post-fetch storage snapshot alone misses that window).
     */
    protected _sessionRemovalEpoch: number;
    /**
     * Keeps track of the async client initialization.
     * When null or not yet resolved the auth state is `unknown`
     * Once resolved the auth state is known and it's safe to call any further client methods.
     * Keep extra care to never reject or throw uncaught errors
     */
    protected initializePromise: Promise<InitializeResult> | null;
    /**
     * Non-null only while `initialize()` is running. While open,
     * `_notifyAllSubscribers` enqueues init-chain notifications (those fired with
     * `broadcast = true`, i.e. from `_recoverAndRefresh`) into this array instead
     * of firing directly, so that `initializePromise` is guaranteed to be
     * resolved before any subscriber callback runs. Callbacks that call
     * `getSession()` / `getUser()` etc. would otherwise deadlock because those
     * methods await `initializePromise`. Notifications from the incoming
     * BroadcastChannel handler (`broadcast = false`) are not enqueued — they fire
     * immediately. Flushed (in order) by `initialize()` after `initializePromise`
     * settles.
     */
    private _pendingInitNotifications;
    protected detectSessionInUrl: boolean | ((url: URL, params: {
        [parameter: string]: string;
    }) => boolean);
    protected url: string;
    protected headers: {
        [key: string]: string;
    };
    protected hasCustomAuthorizationHeader: boolean;
    protected suppressGetSessionWarning: boolean;
    protected fetch: Fetch;
    /**
     * Custom lock function passed via `settings.lock`. When non-null, every auth
     * operation runs inside `_acquireLock`. When null (the default), the client
     * uses its lockless coordination (refresh single-flight + commit guard).
     * TODO(v3): remove along with the legacy lock path.
     */
    protected lock: LockFunc | null;
    protected lockAcquired: boolean;
    protected pendingInLock: Promise<any>[];
    protected throwOnError: boolean;
    /**
     * Only consulted when a custom `lock` is supplied. TODO(v3): remove.
     */
    protected lockAcquireTimeout: number;
    /**
     * Opt-in flags for experimental features. Defaults to an empty object.
     * See `GoTrueClientOptions.experimental`.
     */
    protected experimental: ExperimentalFeatureFlags;
    /**
     * Used to broadcast state change events to other tabs listening.
     */
    protected broadcastChannel: BroadcastChannel | null;
    protected logDebugMessages: boolean;
    protected logger: (message: string, ...args: any[]) => void;
    /**
     * Create a new client for use in the browser.
     *
     * @example Using supabase-js (recommended)
     * ```ts
     * import { createClient } from '@supabase/supabase-js'
     *
     * const supabase = createClient('https://xyzcompany.supabase.co', 'your-publishable-key')
     * const { data, error } = await supabase.auth.getUser()
     * ```
     *
     * @example Standalone import for bundle-sensitive environments
     * ```ts
     * import { GoTrueClient } from '@supabase/auth-js'
     *
     * const auth = new GoTrueClient({
     *   url: 'https://xyzcompany.supabase.co/auth/v1',
     *   headers: { apikey: 'your-publishable-key' },
     *   storageKey: 'supabase-auth',
     * })
     * ```
     */
    constructor(options: GoTrueClientOptions);
    /**
     * Returns whether error throwing mode is enabled for this client.
     */
    isThrowOnErrorEnabled(): boolean;
    /**
     * Centralizes return handling with optional error throwing. When `throwOnError` is enabled
     * and the provided result contains a non-nullish error, the error is thrown instead of
     * being returned. This ensures consistent behavior across all public API methods.
     */
    private _returnResult;
    private _logPrefix;
    private _debug;
    /**
     * Initialize the auth client by loading the session from storage or
     * detecting it from the URL after an OAuth, magic-link, or password-recovery
     * redirect.
     *
     * **Most callers do not need to invoke this directly.** The client calls it
     * automatically during construction, and to react to sign-in events (including
     * post-redirect events) you should subscribe to `onAuthStateChange` rather
     * than awaiting `initialize()`.
     *
     * You only need to call it manually when you have opted out of the automatic
     * call by passing `skipAutoInitialize: true` — for example, in an SSR context
     * where you need to control initialization timing. In that case, awaiting
     * `initialize()` returns the resolved session result (or any error encountered
     * while detecting it from the URL).
     *
     * @category Auth
     */
    initialize(): Promise<InitializeResult>;
    /**
     * IMPORTANT:
     * 1. Never throw in this method, as it is called from the constructor
     * 2. Never return a session from this method as it would be cached over
     *    the whole lifetime of the client
     */
    private _initialize;
    /**
     * Creates a new anonymous user.
     *
     * @returns A session where the is_anonymous claim in the access token JWT set to true
     *
     * @category Auth
     *
     * @remarks
     * - Returns an anonymous user
     * - It is recommended to set up captcha for anonymous sign-ins to prevent abuse. You can pass in the captcha token in the `options` param.
     *
     * @example Create an anonymous user
     * ```js
     * const { data, error } = await supabase.auth.signInAnonymously({
     *   options: {
     *     captchaToken
     *   }
     * });
     * ```
     *
     * @exampleResponse Create an anonymous user
     * ```json
     * {
     *   "data": {
     *     "user": {
     *       "id": "11111111-1111-1111-1111-111111111111",
     *       "aud": "authenticated",
     *       "role": "authenticated",
     *       "email": "",
     *       "phone": "",
     *       "last_sign_in_at": "2024-01-01T00:00:00Z",
     *       "app_metadata": {},
     *       "user_metadata": {},
     *       "identities": [],
     *       "created_at": "2024-01-01T00:00:00Z",
     *       "updated_at": "2024-01-01T00:00:00Z",
     *       "is_anonymous": true
     *     },
     *     "session": {
     *       "access_token": "<ACCESS_TOKEN>",
     *       "token_type": "bearer",
     *       "expires_in": 3600,
     *       "expires_at": 1700000000,
     *       "refresh_token": "<REFRESH_TOKEN>",
     *       "user": {
     *         "id": "11111111-1111-1111-1111-111111111111",
     *         "aud": "authenticated",
     *         "role": "authenticated",
     *         "email": "",
     *         "phone": "",
     *         "last_sign_in_at": "2024-01-01T00:00:00Z",
     *         "app_metadata": {},
     *         "user_metadata": {},
     *         "identities": [],
     *         "created_at": "2024-01-01T00:00:00Z",
     *         "updated_at": "2024-01-01T00:00:00Z",
     *         "is_anonymous": true
     *       }
     *     }
     *   },
     *   "error": null
     * }
     * ```
     *
     * @example Create an anonymous user with custom user metadata
     * ```js
     * const { data, error } = await supabase.auth.signInAnonymously({
     *   options: {
     *     data
     *   }
     * })
     * ```
     */
    signInAnonymously(credentials?: SignInAnonymouslyCredentials): Promise<AuthResponse>;
    /**
     * Creates a new user.
     *
     * Be aware that if a user account exists in the system you may get back an
     * error message that attempts to hide this information from the user.
     * This method has support for PKCE via email signups. The PKCE flow cannot be used when autoconfirm is enabled.
     *
     * @returns A logged-in session if the server has "autoconfirm" ON
     * @returns A user if the server has "autoconfirm" OFF
     *
     * @category Auth
     *
     * @remarks
     * - By default, the user needs to verify their email address before logging in. To turn this off, disable **Confirm email** in [your project](/dashboard/project/_/auth/providers).
     * - **Confirm email** determines if users need to confirm their email address after signing up.
     *   - If **Confirm email** is enabled, a `user` is returned but `session` is null.
     *   - If **Confirm email** is disabled, both a `user` and a `session` are returned.
     * - When the user confirms their email address, they are redirected to the [`SITE_URL`](/docs/guides/auth/redirect-urls#use-wildcards-in-redirect-urls) by default. You can modify your `SITE_URL` or add additional redirect URLs in [your project](/dashboard/project/_/auth/url-configuration).
     * - If signUp() is called for an existing confirmed user:
     *   - When both **Confirm email** and **Confirm phone** (even when phone provider is disabled) are enabled in [your project](/dashboard/project/_/auth/providers), an obfuscated/fake user object is returned.
     *   - When either **Confirm email** or **Confirm phone** (even when phone provider is disabled) is disabled, the error message, `User already registered` is returned.
     * - To fetch the currently logged-in user, refer to [`getUser()`](/docs/reference/javascript/auth-getuser).
     *
     * @example Sign up with an email and password
     * ```js
     * const { data, error } = await supabase.auth.signUp({
     *   email: 'example@email.com',
     *   password: 'example-password',
     * })
     * ```
     *
     * @exampleResponse Sign up with an email and password
     * ```json
     * // Some fields may be null if "confirm email" is enabled.
     * {
     *   "data": {
     *     "user": {
     *       "id": "11111111-1111-1111-1111-111111111111",
     *       "aud": "authenticated",
     *       "role": "authenticated",
     *       "email": "example@email.com",
     *       "email_confirmed_at": "2024-01-01T00:00:00Z",
     *       "phone": "",
     *       "last_sign_in_at": "2024-01-01T00:00:00Z",
     *       "app_metadata": {
     *         "provider": "email",
     *         "providers": [
     *           "email"
     *         ]
     *       },
     *       "user_metadata": {},
     *       "identities": [
     *         {
     *           "identity_id": "22222222-2222-2222-2222-222222222222",
     *           "id": "11111111-1111-1111-1111-111111111111",
     *           "user_id": "11111111-1111-1111-1111-111111111111",
     *           "identity_data": {
     *             "email": "example@email.com",
     *             "email_verified": false,
     *             "phone_verified": false,
     *             "sub": "11111111-1111-1111-1111-111111111111"
     *           },
     *           "provider": "email",
     *           "last_sign_in_at": "2024-01-01T00:00:00Z",
     *           "created_at": "2024-01-01T00:00:00Z",
     *           "updated_at": "2024-01-01T00:00:00Z",
     *           "email": "example@email.com"
     *         }
     *       ],
     *       "created_at": "2024-01-01T00:00:00Z",
     *       "updated_at": "2024-01-01T00:00:00Z"
     *     },
     *     "session": {
     *       "access_token": "<ACCESS_TOKEN>",
     *       "token_type": "bearer",
     *       "expires_in": 3600,
     *       "expires_at": 1700000000,
     *       "refresh_token": "<REFRESH_TOKEN>",
     *       "user": {
     *         "id": "11111111-1111-1111-1111-111111111111",
     *         "aud": "authenticated",
     *         "role": "authenticated",
     *         "email": "example@email.com",
     *         "email_confirmed_at": "2024-01-01T00:00:00Z",
     *         "phone": "",
     *         "last_sign_in_at": "2024-01-01T00:00:00Z",
     *         "app_metadata": {
     *           "provider": "email",
     *           "providers": [
     *             "email"
     *           ]
     *         },
     *         "user_metadata": {},
     *         "identities": [
     *           {
     *             "identity_id": "22222222-2222-2222-2222-222222222222",
     *             "id": "11111111-1111-1111-1111-111111111111",
     *             "user_id": "11111111-1111-1111-1111-111111111111",
     *             "identity_data": {
     *               "email": "example@email.com",
     *               "email_verified": false,
     *               "phone_verified": false,
     *               "sub": "11111111-1111-1111-1111-111111111111"
     *             },
     *             "provider": "email",
     *             "last_sign_in_at": "2024-01-01T00:00:00Z",
     *             "created_at": "2024-01-01T00:00:00Z",
     *             "updated_at": "2024-01-01T00:00:00Z",
     *             "email": "example@email.com"
     *           }
     *         ],
     *         "created_at": "2024-01-01T00:00:00Z",
     *         "updated_at": "2024-01-01T00:00:00Z"
     *       }
     *     }
     *   },
     *   "error": null
     * }
     * ```
     *
     * @example Sign up with a phone number and password (SMS)
     * ```js
     * const { data, error } = await supabase.auth.signUp({
     *   phone: '123456789',
     *   password: 'example-password',
     *   options: {
     *     channel: 'sms'
     *   }
     * })
     * ```
     *
     * @exampleDescription Sign up with a phone number and password (whatsapp)
     * The user will be sent a WhatsApp message which contains a OTP. By default, a given user can only request a OTP once every 60 seconds. Note that a user will need to have a valid WhatsApp account that is linked to Twilio in order to use this feature.
     *
     * @example Sign up with a phone number and password (whatsapp)
     * ```js
     * const { data, error } = await supabase.auth.signUp({
     *   phone: '123456789',
     *   password: 'example-password',
     *   options: {
     *     channel: 'whatsapp'
     *   }
     * })
     * ```
     *
     * @example Sign up with additional user metadata
     * ```js
     * const { data, error } = await supabase.auth.signUp(
     *   {
     *     email: 'example@email.com',
     *     password: 'example-password',
     *     options: {
     *       data: {
     *         first_name: 'John',
     *         age: 27,
     *       }
     *     }
     *   }
     * )
     * ```
     *
     * @exampleDescription Sign up with a redirect URL
     * - See [redirect URLs and wildcards](/docs/guides/auth/redirect-urls#use-wildcards-in-redirect-urls) to add additional redirect URLs to your project.
     *
     * @example Sign up with a redirect URL
     * ```js
     * const { data, error } = await supabase.auth.signUp(
     *   {
     *     email: 'example@email.com',
     *     password: 'example-password',
     *     options: {
     *       emailRedirectTo: 'https://example.com/welcome'
     *     }
     *   }
     * )
     * ```
     */
    signUp(credentials: SignUpWithPasswordCredentials): Promise<AuthResponse>;
    /**
     * Log in an existing user with an email and password or phone and password.
     *
     * Be aware that you may get back an error message that will not distinguish
     * between the cases where the account does not exist or that the
     * email/phone and password combination is wrong or that the account can only
     * be accessed via social login.
     *
     * @category Auth
     *
     * @remarks
     * - Requires either an email and password or a phone number and password.
     *
     * @example Sign in with email and password
     * ```js
     * const { data, error } = await supabase.auth.signInWithPassword({
     *   email: 'example@email.com',
     *   password: 'example-password',
     * })
     * ```
     *
     * @exampleResponse Sign in with email and password
     * ```json
     * {
     *   "data": {
     *     "user": {
     *       "id": "11111111-1111-1111-1111-111111111111",
     *       "aud": "authenticated",
     *       "role": "authenticated",
     *       "email": "example@email.com",
     *       "email_confirmed_at": "2024-01-01T00:00:00Z",
     *       "phone": "",
     *       "last_sign_in_at": "2024-01-01T00:00:00Z",
     *       "app_metadata": {
     *         "provider": "email",
     *         "providers": [
     *           "email"
     *         ]
     *       },
     *       "user_metadata": {},
     *       "identities": [
     *         {
     *           "identity_id": "22222222-2222-2222-2222-222222222222",
     *           "id": "11111111-1111-1111-1111-111111111111",
     *           "user_id": "11111111-1111-1111-1111-111111111111",
     *           "identity_data": {
     *             "email": "example@email.com",
     *             "email_verified": false,
     *             "phone_verified": false,
     *             "sub": "11111111-1111-1111-1111-111111111111"
     *           },
     *           "provider": "email",
     *           "last_sign_in_at": "2024-01-01T00:00:00Z",
     *           "created_at": "2024-01-01T00:00:00Z",
     *           "updated_at": "2024-01-01T00:00:00Z",
     *           "email": "example@email.com"
     *         }
     *       ],
     *       "created_at": "2024-01-01T00:00:00Z",
     *       "updated_at": "2024-01-01T00:00:00Z"
     *     },
     *     "session": {
     *       "access_token": "<ACCESS_TOKEN>",
     *       "token_type": "bearer",
     *       "expires_in": 3600,
     *       "expires_at": 1700000000,
     *       "refresh_token": "<REFRESH_TOKEN>",
     *       "user": {
     *         "id": "11111111-1111-1111-1111-111111111111",
     *         "aud": "authenticated",
     *         "role": "authenticated",
     *         "email": "example@email.com",
     *         "email_confirmed_at": "2024-01-01T00:00:00Z",
     *         "phone": "",
     *         "last_sign_in_at": "2024-01-01T00:00:00Z",
     *         "app_metadata": {
     *           "provider": "email",
     *           "providers": [
     *             "email"
     *           ]
     *         },
     *         "user_metadata": {},
     *         "identities": [
     *           {
     *             "identity_id": "22222222-2222-2222-2222-222222222222",
     *             "id": "11111111-1111-1111-1111-111111111111",
     *             "user_id": "11111111-1111-1111-1111-111111111111",
     *             "identity_data": {
     *               "email": "example@email.com",
     *               "email_verified": false,
     *               "phone_verified": false,
     *               "sub": "11111111-1111-1111-1111-111111111111"
     *             },
     *             "provider": "email",
     *             "last_sign_in_at": "2024-01-01T00:00:00Z",
     *             "created_at": "2024-01-01T00:00:00Z",
     *             "updated_at": "2024-01-01T00:00:00Z",
     *             "email": "example@email.com"
     *           }
     *         ],
     *         "created_at": "2024-01-01T00:00:00Z",
     *         "updated_at": "2024-01-01T00:00:00Z"
     *       }
     *     }
     *   },
     *   "error": null
     * }
     * ```
     *
     * @example Sign in with phone and password
     * ```js
     * const { data, error } = await supabase.auth.signInWithPassword({
     *   phone: '+13334445555',
     *   password: 'some-password',
     * })
     * ```
     *
     * @exampleDescription Handling errors
     * Log the full `error` object so fields like `code`, `status`, and `name` aren't hidden. The `error.code` (e.g. `'invalid_credentials'`, `'email_not_confirmed'`) is often more useful for branching than `error.message`, and the full object surfaces both.
     *
     * @example Handling errors
     * ```js
     * const { data, error } = await supabase.auth.signInWithPassword({
     *   email: 'example@email.com',
     *   password: 'example-password',
     * })
     * if (error) {
     *   console.error(error)
     *   return
     * }
     * ```
     */
    signInWithPassword(credentials: SignInWithPasswordCredentials): Promise<AuthTokenResponsePassword>;
    /**
     * Log in an existing user via a third-party provider.
     * This method supports the PKCE flow.
     *
     * @category Auth
     *
     * @remarks
     * - This method is used for signing in using [Social Login (OAuth) providers](/docs/guides/auth#configure-third-party-providers).
     * - It works by redirecting your application to the provider's authorization screen, before bringing back the user to your app.
     *
     * @example Sign in using a third-party provider
     * ```js
     * const { data, error } = await supabase.auth.signInWithOAuth({
     *   provider: 'github'
     * })
     * ```
     *
     * @exampleResponse Sign in using a third-party provider
     * ```json
     * {
     *   data: {
     *     provider: 'github',
     *     url: <PROVIDER_URL_TO_REDIRECT_TO>,
     *     flowId: <PKCE_FLOW_ID_OR_NULL>
     *   },
     *   error: null
     * }
     * ```
     *
     * @exampleDescription Sign in using a third-party provider with redirect
     * - When the OAuth provider successfully authenticates the user, they are redirected to the URL specified in the `redirectTo` parameter. This parameter defaults to the [`SITE_URL`](/docs/guides/auth/redirect-urls#use-wildcards-in-redirect-urls). It does not redirect the user immediately after invoking this method.
     * - See [redirect URLs and wildcards](/docs/guides/auth/redirect-urls#use-wildcards-in-redirect-urls) to add additional redirect URLs to your project.
     *
     * @example Sign in using a third-party provider with redirect
     * ```js
     * const { data, error } = await supabase.auth.signInWithOAuth({
     *   provider: 'github',
     *   options: {
     *     redirectTo: 'https://example.com/welcome'
     *   }
     * })
     * ```
     *
     * @exampleDescription Sign in with scopes and access provider tokens
     * If you need additional access from an OAuth provider, in order to access provider specific APIs in the name of the user, you can do this by passing in the scopes the user should authorize for your application. Note that the `scopes` option takes in **a space-separated list** of scopes.
     *
     * Because OAuth sign-in often includes redirects, you should register an `onAuthStateChange` callback immediately after you create the Supabase client. This callback will listen for the presence of `provider_token` and `provider_refresh_token` properties on the `session` object and store them in local storage. The client library will emit these values **only once** immediately after the user signs in. You can then access them by looking them up in local storage, or send them to your backend servers for further processing.
     *
     * Finally, make sure you remove them from local storage on the `SIGNED_OUT` event. If the OAuth provider supports token revocation, make sure you call those APIs either from the frontend or schedule them to be called on the backend.
     *
     * @example Sign in with scopes and access provider tokens
     * ```js
     * // Register this immediately after calling createClient!
     * // Because signInWithOAuth causes a redirect, you need to fetch the
     * // provider tokens from the callback.
     * supabase.auth.onAuthStateChange((event, session) => {
     *   if (session && session.provider_token) {
     *     window.localStorage.setItem('oauth_provider_token', session.provider_token)
     *   }
     *
     *   if (session && session.provider_refresh_token) {
     *     window.localStorage.setItem('oauth_provider_refresh_token', session.provider_refresh_token)
     *   }
     *
     *   if (event === 'SIGNED_OUT') {
     *     window.localStorage.removeItem('oauth_provider_token')
     *     window.localStorage.removeItem('oauth_provider_refresh_token')
     *   }
     * })
     *
     * // Call this on your Sign in with GitHub button to initiate OAuth
     * // with GitHub with the requested elevated scopes.
     * await supabase.auth.signInWithOAuth({
     *   provider: 'github',
     *   options: {
     *     scopes: 'repo gist notifications'
     *   }
     * })
     * ```
     */
    signInWithOAuth(credentials: SignInWithOAuthCredentials): Promise<OAuthResponse>;
    /**
     * Log in an existing user by exchanging an Auth Code issued during the PKCE flow.
     *
     * @category Auth
     *
     * @remarks
     * - Used when `flowType` is set to `pkce` in client options.
     * - When several PKCE flows are in flight at once, pass `options.flowId` so
     *   the code is exchanged with the verifier created by that specific flow.
     *   The flow id is returned by `signInWithOAuth`, and with
     *   `experimental.appendPkceFlowIdToRedirects` enabled it also arrives on
     *   your callback URL as the reserved `sb_flow_id` query parameter (read
     *   automatically in a browser).
     * - When a flow id is present but its stored verifier is gone (evicted,
     *   already used, or from another device), the call fails with a verifier
     *   missing error instead of trying another flow's verifier — a mismatched
     *   verifier would consume the single-use code. Without any flow id the
     *   most recently stored verifier is used, as before.
     *
     * @example Exchange Auth Code
     * ```js
     * supabase.auth.exchangeCodeForSession('34e770dd-9ff9-416c-87fa-43b31d7ef225')
     * ```
     *
     * @example Exchange Auth Code for a specific flow (e.g. in a server-side callback handler)
     * ```js
     * const flowId = requestUrl.searchParams.get('sb_flow_id')
     * supabase.auth.exchangeCodeForSession(code, flowId ? { flowId } : undefined)
     * ```
     *
     * @exampleResponse Exchange Auth Code
     * ```json
     * {
     *   "data": {
     *     session: {
     *       access_token: '<ACCESS_TOKEN>',
     *       token_type: 'bearer',
     *       expires_in: 3600,
     *       expires_at: 1700000000,
     *       refresh_token: '<REFRESH_TOKEN>',
     *       user: {
     *         id: '11111111-1111-1111-1111-111111111111',
     *         aud: 'authenticated',
     *         role: 'authenticated',
     *         email: 'example@email.com'
     *         email_confirmed_at: '2024-01-01T00:00:00Z',
     *         phone: '',
     *         confirmation_sent_at: '2024-01-01T00:00:00Z',
     *         confirmed_at: '2024-01-01T00:00:00Z',
     *         last_sign_in_at: '2024-01-01T00:00:00Z',
     *         app_metadata: {
     *           "provider": "email",
     *           "providers": [
     *             "email",
     *             "<OTHER_PROVIDER>"
     *           ]
     *         },
     *         user_metadata: {
     *           email: 'email@email.com',
     *           email_verified: true,
     *           full_name: 'User Name',
     *           iss: '<ISS>',
     *           name: 'User Name',
     *           phone_verified: false,
     *           provider_id: '<PROVIDER_ID>',
     *           sub: '<SUB>'
     *         },
     *         identities: [
     *           {
     *             "identity_id": "22222222-2222-2222-2222-222222222222",
     *             "id": "11111111-1111-1111-1111-111111111111",
     *             "user_id": "11111111-1111-1111-1111-111111111111",
     *             "identity_data": {
     *               "email": "example@email.com",
     *               "email_verified": false,
     *               "phone_verified": false,
     *               "sub": "11111111-1111-1111-1111-111111111111"
     *             },
     *             "provider": "email",
     *             "last_sign_in_at": "2024-01-01T00:00:00Z",
     *             "created_at": "2024-01-01T00:00:00Z",
     *             "updated_at": "2024-01-01T00:00:00Z",
     *             "email": "email@example.com"
     *           },
     *           {
     *             "identity_id": "33333333-3333-3333-3333-333333333333",
     *             "id": "<ID>",
     *             "user_id": "<USER_ID>",
     *             "identity_data": {
     *               "email": "example@email.com",
     *               "email_verified": true,
     *               "full_name": "User Name",
     *               "iss": "<ISS>",
     *               "name": "User Name",
     *               "phone_verified": false,
     *               "provider_id": "<PROVIDER_ID>",
     *               "sub": "<SUB>"
     *             },
     *             "provider": "<PROVIDER>",
     *             "last_sign_in_at": "2024-01-01T00:00:00Z",
     *             "created_at": "2024-01-01T00:00:00Z",
     *             "updated_at": "2024-01-01T00:00:00Z",
     *             "email": "example@email.com"
     *           }
     *         ],
     *         created_at: '2024-01-01T00:00:00Z',
     *         updated_at: '2024-01-01T00:00:00Z',
     *         is_anonymous: false
     *       },
     *       provider_token: '<PROVIDER_TOKEN>',
     *       provider_refresh_token: '<PROVIDER_REFRESH_TOKEN>'
     *     },
     *     user: {
     *       id: '11111111-1111-1111-1111-111111111111',
     *       aud: 'authenticated',
     *       role: 'authenticated',
     *       email: 'example@email.com',
     *       email_confirmed_at: '2024-01-01T00:00:00Z',
     *       phone: '',
     *       confirmation_sent_at: '2024-01-01T00:00:00Z',
     *       confirmed_at: '2024-01-01T00:00:00Z',
     *       last_sign_in_at: '2024-01-01T00:00:00Z',
     *       app_metadata: {
     *         provider: 'email',
     *         providers: [
     *           "email",
     *           "<OTHER_PROVIDER>"
     *         ]
     *       },
     *       user_metadata: {
     *         email: 'email@email.com',
     *         email_verified: true,
     *         full_name: 'User Name',
     *         iss: '<ISS>',
     *         name: 'User Name',
     *         phone_verified: false,
     *         provider_id: '<PROVIDER_ID>',
     *         sub: '<SUB>'
     *       },
     *       identities: [
     *         {
     *           "identity_id": "22222222-2222-2222-2222-222222222222",
     *           "id": "11111111-1111-1111-1111-111111111111",
     *           "user_id": "11111111-1111-1111-1111-111111111111",
     *           "identity_data": {
     *             "email": "example@email.com",
     *             "email_verified": false,
     *             "phone_verified": false,
     *             "sub": "11111111-1111-1111-1111-111111111111"
     *           },
     *           "provider": "email",
     *           "last_sign_in_at": "2024-01-01T00:00:00Z",
     *           "created_at": "2024-01-01T00:00:00Z",
     *           "updated_at": "2024-01-01T00:00:00Z",
     *           "email": "email@example.com"
     *         },
     *         {
     *           "identity_id": "33333333-3333-3333-3333-333333333333",
     *           "id": "<ID>",
     *           "user_id": "<USER_ID>",
     *           "identity_data": {
     *             "email": "example@email.com",
     *             "email_verified": true,
     *             "full_name": "User Name",
     *             "iss": "<ISS>",
     *             "name": "User Name",
     *             "phone_verified": false,
     *             "provider_id": "<PROVIDER_ID>",
     *             "sub": "<SUB>"
     *           },
     *           "provider": "<PROVIDER>",
     *           "last_sign_in_at": "2024-01-01T00:00:00Z",
     *           "created_at": "2024-01-01T00:00:00Z",
     *           "updated_at": "2024-01-01T00:00:00Z",
     *           "email": "example@email.com"
     *         }
     *       ],
     *       created_at: '2024-01-01T00:00:00Z',
     *       updated_at: '2024-01-01T00:00:00Z',
     *       is_anonymous: false
     *     },
     *     redirectType: null
     *   },
     *   "error": null
     * }
     * ```
     */
    exchangeCodeForSession(authCode: string, options?: {
        flowId?: string;
    }): Promise<AuthTokenResponse>;
    /**
     * Signs in a user by verifying a message signed by the user's private key.
     * Supports Ethereum (via Sign-In-With-Ethereum) & Solana (Sign-In-With-Solana) standards,
     * both of which derive from the EIP-4361 standard
     * With slight variation on Solana's side.
     * @reference https://eips.ethereum.org/EIPS/eip-4361
     *
     * @category Auth
     *
     * @remarks
     * - Uses a Web3 (Ethereum, Solana) wallet to sign a user in.
     * - Read up on the [potential for abuse](/docs/guides/auth/auth-web3#potential-for-abuse) before using it.
     *
     * @example Sign in with Solana or Ethereum (Window API)
     * ```js
     *   // uses window.ethereum for the wallet
     *   const { data, error } = await supabase.auth.signInWithWeb3({
     *     chain: 'ethereum',
     *     statement: 'I accept the Terms of Service at https://example.com/tos'
     *   })
     *
     *   // uses window.solana for the wallet
     *   const { data, error } = await supabase.auth.signInWithWeb3({
     *     chain: 'solana',
     *     statement: 'I accept the Terms of Service at https://example.com/tos'
     *   })
     * ```
     *
     * @example Sign in with Ethereum (Message and Signature)
     * ```js
     *   const { data, error } = await supabase.auth.signInWithWeb3({
     *     chain: 'ethereum',
     *     message: '<sign in with ethereum message>',
     *     signature: '<hex of the ethereum signature over the message>',
     *   })
     * ```
     *
     * @example Sign in with Solana (Brave)
     * ```js
     *   const { data, error } = await supabase.auth.signInWithWeb3({
     *     chain: 'solana',
     *     statement: 'I accept the Terms of Service at https://example.com/tos',
     *     wallet: window.braveSolana
     *   })
     * ```
     *
     * @example Sign in with Solana (Wallet Adapter)
     * ```jsx
     *   function SignInButton() {
     *   const wallet = useWallet()
     *
     *   return (
     *     <>
     *       {wallet.connected ? (
     *         <button
     *           onClick={() => {
     *             supabase.auth.signInWithWeb3({
     *               chain: 'solana',
     *               statement: 'I accept the Terms of Service at https://example.com/tos',
     *               wallet,
     *             })
     *           }}
     *         >
     *           Sign in with Solana
     *         </button>
     *       ) : (
     *         <WalletMultiButton />
     *       )}
     *     </>
     *   )
     * }
     *
     * function App() {
     *   const endpoint = clusterApiUrl('devnet')
     *   const wallets = useMemo(() => [], [])
     *
     *   return (
     *     <ConnectionProvider endpoint={endpoint}>
     *       <WalletProvider wallets={wallets}>
     *         <WalletModalProvider>
     *           <SignInButton />
     *         </WalletModalProvider>
     *       </WalletProvider>
     *     </ConnectionProvider>
     *   )
     * }
     * ```
     */
    signInWithWeb3(credentials: Web3Credentials): Promise<{
        data: {
            session: Session;
            user: User;
        };
        error: null;
    } | {
        data: {
            session: null;
            user: null;
        };
        error: AuthError;
    }>;
    private signInWithEthereum;
    private signInWithSolana;
    private _exchangeCodeForSession;
    /**
     * Allows signing in with an OIDC ID token. The authentication provider used
     * should be enabled and configured.
     *
     * @category Auth
     *
     * @remarks
     * - Use an ID token to sign in.
     * - Especially useful when implementing sign in using native platform dialogs in mobile or desktop apps using Sign in with Apple or Sign in with Google on iOS and Android.
     * - You can also use Google's [One Tap](https://developers.google.com/identity/gsi/web/guides/display-google-one-tap) and [Automatic sign-in](https://developers.google.com/identity/gsi/web/guides/automatic-sign-in-sign-out) via this API.
     *
     * @example Sign In using ID Token
     * ```js
     * const { data, error } = await supabase.auth.signInWithIdToken({
     *   provider: 'google',
     *   token: 'your-id-token'
     * })
     * ```
     *
     * @exampleResponse Sign In using ID Token
     * ```json
     * {
     *   "data": {
     *     "user": {
     *       "id": "11111111-1111-1111-1111-111111111111",
     *       "aud": "authenticated",
     *       "role": "authenticated",
     *       "last_sign_in_at": "2024-01-01T00:00:00Z",
     *       "app_metadata": {
     *         ...
     *       },
     *       "user_metadata": {
     *         ...
     *       },
     *       "identities": [
     *         {
     *           "identity_id": "22222222-2222-2222-2222-222222222222",
     *           "provider": "google",
     *         }
     *       ],
     *       "created_at": "2024-01-01T00:00:00Z",
     *       "updated_at": "2024-01-01T00:00:00Z",
     *     },
     *     "session": {
     *       "access_token": "<ACCESS_TOKEN>",
     *       "token_type": "bearer",
     *       "expires_in": 3600,
     *       "expires_at": 1700000000,
     *       "refresh_token": "<REFRESH_TOKEN>",
     *       "user": {
     *         "id": "11111111-1111-1111-1111-111111111111",
     *         "aud": "authenticated",
     *         "role": "authenticated",
     *         "last_sign_in_at": "2024-01-01T00:00:00Z",
     *         "app_metadata": {
     *           ...
     *         },
     *         "user_metadata": {
     *           ...
     *         },
     *         "identities": [
     *           {
     *             "identity_id": "22222222-2222-2222-2222-222222222222",
     *             "provider": "google",
     *           }
     *         ],
     *         "created_at": "2024-01-01T00:00:00Z",
     *         "updated_at": "2024-01-01T00:00:00Z",
     *       }
     *     }
     *   },
     *   "error": null
     * }
     * ```
     */
    signInWithIdToken(credentials: SignInWithIdTokenCredentials): Promise<AuthTokenResponse>;
    /**
     * Log in a user using magiclink or a one-time password (OTP).
     *
     * If the `{{ .ConfirmationURL }}` variable is specified in the email template, a magiclink will be sent.
     * If the `{{ .Token }}` variable is specified in the email template, an OTP will be sent.
     * If you're using phone sign-ins, only an OTP will be sent. You won't be able to send a magiclink for phone sign-ins.
     *
     * Be aware that you may get back an error message that will not distinguish
     * between the cases where the account does not exist or, that the account
     * can only be accessed via social login.
     *
     * Do note that you will need to configure a Whatsapp sender on Twilio
     * if you are using phone sign in with the 'whatsapp' channel. The whatsapp
     * channel is not supported on other providers
     * at this time.
     * This method supports PKCE when an email is passed.
     *
     * @category Auth
     *
     * @remarks
     * - Requires either an email or phone number.
     * - This method is used for passwordless sign-ins where a OTP is sent to the user's email or phone number.
     * - If the user doesn't exist, `signInWithOtp()` will signup the user instead. To restrict this behavior, you can set `shouldCreateUser` in `SignInWithPasswordlessCredentials.options` to `false`.
     * - If you're using an email, you can configure whether you want the user to receive a magiclink or a OTP.
     * - If you're using phone, you can configure whether you want the user to receive a OTP.
     * - The magic link's destination URL is determined by the [`SITE_URL`](/docs/guides/auth/redirect-urls#use-wildcards-in-redirect-urls).
     * - See [redirect URLs and wildcards](/docs/guides/auth/redirect-urls#use-wildcards-in-redirect-urls) to add additional redirect URLs to your project.
     * - Magic links and OTPs share the same implementation. To send users a one-time code instead of a magic link, [modify the magic link email template](/dashboard/project/_/auth/templates) to include `{{ .Token }}` instead of `{{ .ConfirmationURL }}`.
     * - See our [Twilio Phone Auth Guide](/docs/guides/auth/phone-login?showSMSProvider=Twilio) for details about configuring WhatsApp sign in.
     *
     * @exampleDescription Sign in with email
     * The user will be sent an email which contains either a magiclink or a OTP or both. By default, a given user can only request a OTP once every 60 seconds.
     *
     * @example Sign in with email
     * ```js
     * const { data, error } = await supabase.auth.signInWithOtp({
     *   email: 'example@email.com',
     *   options: {
     *     emailRedirectTo: 'https://example.com/welcome'
     *   }
     * })
     * ```
     *
     * @exampleResponse Sign in with email
     * ```json
     * {
     *   "data": {
     *     "user": null,
     *     "session": null
     *   },
     *   "error": null
     * }
     * ```
     *
     * @exampleDescription Sign in with SMS OTP
     * The user will be sent a SMS which contains a OTP. By default, a given user can only request a OTP once every 60 seconds.
     *
     * @example Sign in with SMS OTP
     * ```js
     * const { data, error } = await supabase.auth.signInWithOtp({
     *   phone: '+13334445555',
     * })
     * ```
     *
     * @exampleDescription Sign in with WhatsApp OTP
     * The user will be sent a WhatsApp message which contains a OTP. By default, a given user can only request a OTP once every 60 seconds. Note that a user will need to have a valid WhatsApp account that is linked to Twilio in order to use this feature.
     *
     * @example Sign in with WhatsApp OTP
     * ```js
     * const { data, error } = await supabase.auth.signInWithOtp({
     *   phone: '+13334445555',
     *   options: {
     *     channel:'whatsapp',
     *   }
     * })
     * ```
     */
    signInWithOtp(credentials: SignInWithPasswordlessCredentials): Promise<AuthOtpResponse>;
    /**
     * Log in a user given a User supplied OTP or TokenHash received through mobile or email.
     *
     * @category Auth
     *
     * @remarks
     * - The `verifyOtp` method takes in different verification types.
     * - If a phone number is used, the type can either be:
     *   1. `sms` – Used when verifying a one-time password (OTP) sent via SMS during sign-up or sign-in.
     *   2. `phone_change` – Used when verifying an OTP sent to a new phone number during a phone number update process.
     * - If an email address is used, the type can be one of the following (note: `signup` and `magiclink` types are deprecated):
     *   1. `email` – Used when verifying an OTP sent to the user's email during sign-up or sign-in.
     *   2. `recovery` – Used when verifying an OTP sent for account recovery, typically after a password reset request.
     *   3. `invite` – Used when verifying an OTP sent as part of an invitation to join a project or organization.
     *   4. `email_change` – Used when verifying an OTP sent to a new email address during an email update process.
     * - The verification type used should be determined based on the corresponding auth method called before `verifyOtp` to sign up / sign-in a user.
     * - The `TokenHash` is contained in the [email templates](/docs/guides/auth/auth-email-templates) and can be used to sign in.  You may wish to use the hash for the PKCE flow for Server Side Auth. Read [the Password-based Auth guide](/docs/guides/auth/passwords) for more details.
     *
     * @example Verify Signup One-Time Password (OTP)
     * ```js
     * const { data, error } = await supabase.auth.verifyOtp({ email, token, type: 'email'})
     * ```
     *
     * @exampleResponse Verify Signup One-Time Password (OTP)
     * ```json
     * {
     *   "data": {
     *     "user": {
     *       "id": "11111111-1111-1111-1111-111111111111",
     *       "aud": "authenticated",
     *       "role": "authenticated",
     *       "email": "example@email.com",
     *       "email_confirmed_at": "2024-01-01T00:00:00Z",
     *       "phone": "",
     *       "confirmed_at": "2024-01-01T00:00:00Z",
     *       "recovery_sent_at": "2024-01-01T00:00:00Z",
     *       "last_sign_in_at": "2024-01-01T00:00:00Z",
     *       "app_metadata": {
     *         "provider": "email",
     *         "providers": [
     *           "email"
     *         ]
     *       },
     *       "user_metadata": {
     *         "email": "example@email.com",
     *         "email_verified": false,
     *         "phone_verified": false,
     *         "sub": "11111111-1111-1111-1111-111111111111"
     *       },
     *       "identities": [
     *         {
     *           "identity_id": "22222222-2222-2222-2222-222222222222",
     *           "id": "11111111-1111-1111-1111-111111111111",
     *           "user_id": "11111111-1111-1111-1111-111111111111",
     *           "identity_data": {
     *             "email": "example@email.com",
     *             "email_verified": false,
     *             "phone_verified": false,
     *             "sub": "11111111-1111-1111-1111-111111111111"
     *           },
     *           "provider": "email",
     *           "last_sign_in_at": "2024-01-01T00:00:00Z",
     *           "created_at": "2024-01-01T00:00:00Z",
     *           "updated_at": "2024-01-01T00:00:00Z",
     *           "email": "example@email.com"
     *         }
     *       ],
     *       "created_at": "2024-01-01T00:00:00Z",
     *       "updated_at": "2024-01-01T00:00:00Z",
     *       "is_anonymous": false
     *     },
     *     "session": {
     *       "access_token": "<ACCESS_TOKEN>",
     *       "token_type": "bearer",
     *       "expires_in": 3600,
     *       "expires_at": 1700000000,
     *       "refresh_token": "<REFRESH_TOKEN>",
     *       "user": {
     *         "id": "11111111-1111-1111-1111-111111111111",
     *         "aud": "authenticated",
     *         "role": "authenticated",
     *         "email": "example@email.com",
     *         "email_confirmed_at": "2024-01-01T00:00:00Z",
     *         "phone": "",
     *         "confirmed_at": "2024-01-01T00:00:00Z",
     *         "recovery_sent_at": "2024-01-01T00:00:00Z",
     *         "last_sign_in_at": "2024-01-01T00:00:00Z",
     *         "app_metadata": {
     *           "provider": "email",
     *           "providers": [
     *             "email"
     *           ]
     *         },
     *         "user_metadata": {
     *           "email": "example@email.com",
     *           "email_verified": false,
     *           "phone_verified": false,
     *           "sub": "11111111-1111-1111-1111-111111111111"
     *         },
     *         "identities": [
     *           {
     *             "identity_id": "22222222-2222-2222-2222-222222222222",
     *             "id": "11111111-1111-1111-1111-111111111111",
     *             "user_id": "11111111-1111-1111-1111-111111111111",
     *             "identity_data": {
     *               "email": "example@email.com",
     *               "email_verified": false,
     *               "phone_verified": false,
     *               "sub": "11111111-1111-1111-1111-111111111111"
     *             },
     *             "provider": "email",
     *             "last_sign_in_at": "2024-01-01T00:00:00Z",
     *             "created_at": "2024-01-01T00:00:00Z",
     *             "updated_at": "2024-01-01T00:00:00Z",
     *             "email": "example@email.com"
     *           }
     *         ],
     *         "created_at": "2024-01-01T00:00:00Z",
     *         "updated_at": "2024-01-01T00:00:00Z",
     *         "is_anonymous": false
     *       }
     *     }
     *   },
     *   "error": null
     * }
     * ```
     *
     * @example Verify SMS One-Time Password (OTP)
     * ```js
     * const { data, error } = await supabase.auth.verifyOtp({ phone, token, type: 'sms'})
     * ```
     *
     * @example Verify Email Auth (Token Hash)
     * ```js
     * const { data, error } = await supabase.auth.verifyOtp({ token_hash: tokenHash, type: 'email'})
     * ```
     */
    verifyOtp(params: VerifyOtpParams): Promise<AuthResponse>;
    /**
     * Attempts a single-sign on using an enterprise Identity Provider. A
     * successful SSO attempt will redirect the current page to the identity
     * provider authorization page. The redirect URL is implementation and SSO
     * protocol specific.
     *
     * You can use it by providing a SSO domain. Typically you can extract this
     * domain by asking users for their email address. If this domain is
     * registered on the Auth instance the redirect will use that organization's
     * currently active SSO Identity Provider for the login.
     *
     * If you have built an organization-specific login page, you can use the
     * organization's SSO Identity Provider UUID directly instead.
     *
     * @category Auth
     *
     * @remarks
     * - Before you can call this method you need to [establish a connection](/docs/guides/auth/sso/auth-sso-saml#managing-saml-20-connections) to an identity provider. Use the [CLI commands](/docs/reference/cli/supabase-sso) to do this.
     * - If you've associated an email domain to the identity provider, you can use the `domain` property to start a sign-in flow.
     * - In case you need to use a different way to start the authentication flow with an identity provider, you can use the `providerId` property. For example:
     *     - Mapping specific user email addresses with an identity provider.
     *     - Using different hints to identity the identity provider to be used by the user, like a company-specific page, IP address or other tracking information.
     *
     * @example Sign in with email domain
     * ```js
     *   // You can extract the user's email domain and use it to trigger the
     *   // authentication flow with the correct identity provider.
     *
     *   const { data, error } = await supabase.auth.signInWithSSO({
     *     domain: 'company.com'
     *   })
     *
     *   if (data?.url) {
     *     // redirect the user to the identity provider's authentication flow
     *     window.location.href = data.url
     *   }
     * ```
     *
     * @example Sign in with provider UUID
     * ```js
     *   // Useful when you need to map a user's sign in request according
     *   // to different rules that can't use email domains.
     *
     *   const { data, error } = await supabase.auth.signInWithSSO({
     *     providerId: '21648a9d-8d5a-4555-a9d1-d6375dc14e92'
     *   })
     *
     *   if (data?.url) {
     *     // redirect the user to the identity provider's authentication flow
     *     window.location.href = data.url
     *   }
     * ```
     */
    signInWithSSO(params: SignInWithSSO): Promise<SSOResponse>;
    /**
     * Sends a reauthentication OTP to the user's email or phone number.
     * Requires the user to be signed-in.
     *
     * @category Auth
     *
     * @remarks
     * - This method is used together with `updateUser()` when a user's password needs to be updated.
     * - If you require your user to reauthenticate before updating their password, you need to enable the **Secure password change** option in your [project's email provider settings](/dashboard/project/_/auth/providers).
     * - A user is only require to reauthenticate before updating their password if **Secure password change** is enabled and the user **hasn't recently signed in**. A user is deemed recently signed in if the session was created in the last 24 hours.
     * - This method will send a nonce to the user's email. If the user doesn't have a confirmed email address, the method will send the nonce to the user's confirmed phone number instead.
     * - After receiving the OTP, include it as the `nonce` in your `updateUser()` call to finalize the password change.
     *
     * @exampleDescription Send reauthentication nonce
     * Sends a reauthentication nonce to the user's email or phone number.
     *
     * @example Send reauthentication nonce
     * ```js
     * const { error } = await supabase.auth.reauthenticate()
     * ```
     */
    reauthenticate(): Promise<AuthResponse>;
    private _reauthenticate;
    /**
     * Resends an existing signup confirmation email, email change email, SMS OTP or phone change OTP.
     *
     * @category Auth
     *
     * @remarks
     * - Resends a signup confirmation, email change or phone change email to the user.
     * - Passwordless sign-ins can be resent by calling the `signInWithOtp()` method again.
     * - Password recovery emails can be resent by calling the `resetPasswordForEmail()` method again.
     * - This method will only resend an email or phone OTP to the user if there was an initial signup, email change or phone change request being made(note: For existing users signing in with OTP, you should use `signInWithOtp()` again to resend the OTP).
     * - You can specify a redirect url when you resend an email link using the `emailRedirectTo` option.
     *
     * @exampleDescription Resend an email signup confirmation
     * Resends the email signup confirmation to the user
     *
     * @example Resend an email signup confirmation
     * ```js
     * const { error } = await supabase.auth.resend({
     *   type: 'signup',
     *   email: 'email@example.com',
     *   options: {
     *     emailRedirectTo: 'https://example.com/welcome'
     *   }
     * })
     * ```
     *
     * @exampleDescription Resend a phone signup confirmation
     * Resends the phone signup confirmation email to the user
     *
     * @example Resend a phone signup confirmation
     * ```js
     * const { error } = await supabase.auth.resend({
     *   type: 'sms',
     *   phone: '1234567890'
     * })
     * ```
     *
     * @exampleDescription Resend email change email
     * Resends the email change email to the user
     *
     * @example Resend email change email
     * ```js
     * const { error } = await supabase.auth.resend({
     *   type: 'email_change',
     *   email: 'email@example.com'
     * })
     * ```
     *
     * @exampleDescription Resend phone change OTP
     * Resends the phone change OTP to the user
     *
     * @example Resend phone change OTP
     * ```js
     * const { error } = await supabase.auth.resend({
     *   type: 'phone_change',
     *   phone: '1234567890'
     * })
     * ```
     */
    resend(credentials: ResendParams): Promise<AuthOtpResponse>;
    /**
     * Returns the session, refreshing it if necessary.
     *
     * The session returned can be null if the session is not detected which can happen in the event a user is not signed-in or has logged out.
     *
     * **IMPORTANT:** This method loads values directly from the storage attached
     * to the client. If that storage is based on request cookies for example,
     * the values in it may not be authentic and therefore it's strongly advised
     * against using this method and its results in such circumstances. A warning
     * will be emitted if this is detected. Use {@link GoTrueClient.getUser} instead.
     *
     * @category Auth
     *
     * @remarks
     * - Since the introduction of [asymmetric JWT signing keys](/docs/guides/auth/signing-keys), this method is considered low-level and we encourage you to use `getClaims()` or `getUser()` instead.
     * - Retrieves the current [user session](/docs/guides/auth/sessions) from the storage medium (local storage, cookies).
     * - The session contains an access token (signed JWT), a refresh token and the user object.
     * - If the session's access token is expired or is about to expire, this method will use the refresh token to refresh the session.
     * - When using in a browser, or you've called `startAutoRefresh()` in your environment (React Native, etc.) this function always returns a valid access token without refreshing the session itself, as this is done in the background. This function returns very fast.
     * - **IMPORTANT SECURITY NOTICE:** If using an insecure storage medium, such as cookies or request headers, the user object returned by this function **must not be trusted**. Always verify the JWT using `getClaims()` or your own JWT verification library to securely establish the user's identity and access. You can also use `getUser()` to fetch the user object directly from the Auth server for this purpose.
     * - Cross-tab refresh races are handled by the GoTrue server (the rotated token from the first tab is returned to subsequent tabs via the parent-of-active mechanism), so no client-side serialization is needed.
     *
     * @example Get the session data
     * ```js
     * const { data, error } = await supabase.auth.getSession()
     * ```
     *
     * @exampleResponse Get the session data
     * ```json
     * {
     *   "data": {
     *     "session": {
     *       "access_token": "<ACCESS_TOKEN>",
     *       "token_type": "bearer",
     *       "expires_in": 3600,
     *       "expires_at": 1700000000,
     *       "refresh_token": "<REFRESH_TOKEN>",
     *       "user": {
     *         "id": "11111111-1111-1111-1111-111111111111",
     *         "aud": "authenticated",
     *         "role": "authenticated",
     *         "email": "example@email.com",
     *         "email_confirmed_at": "2024-01-01T00:00:00Z",
     *         "phone": "",
     *         "last_sign_in_at": "2024-01-01T00:00:00Z",
     *         "app_metadata": {
     *           "provider": "email",
     *           "providers": [
     *             "email"
     *           ]
     *         },
     *         "user_metadata": {
     *           "email": "example@email.com",
     *           "email_verified": false,
     *           "phone_verified": false,
     *           "sub": "11111111-1111-1111-1111-111111111111"
     *         },
     *         "identities": [
     *           {
     *             "identity_id": "22222222-2222-2222-2222-222222222222",
     *             "id": "11111111-1111-1111-1111-111111111111",
     *             "user_id": "11111111-1111-1111-1111-111111111111",
     *             "identity_data": {
     *               "email": "example@email.com",
     *               "email_verified": false,
     *               "phone_verified": false,
     *               "sub": "11111111-1111-1111-1111-111111111111"
     *             },
     *             "provider": "email",
     *             "last_sign_in_at": "2024-01-01T00:00:00Z",
     *             "created_at": "2024-01-01T00:00:00Z",
     *             "updated_at": "2024-01-01T00:00:00Z",
     *             "email": "example@email.com"
     *           }
     *         ],
     *         "created_at": "2024-01-01T00:00:00Z",
     *         "updated_at": "2024-01-01T00:00:00Z",
     *         "is_anonymous": false
     *       }
     *     }
     *   },
     *   "error": null
     * }
     * ```
     */
    getSession(): Promise<{
        data: {
            session: Session;
        };
        error: null;
    } | {
        data: {
            session: null;
        };
        error: AuthError;
    } | {
        data: {
            session: null;
        };
        error: null;
    }>;
    /**
     * Acquires a global lock based on the storage key.
     *
     * TODO(v3): remove along with the legacy lock path. Only called when
     * `this.lock` is non-null (custom lock supplied via constructor). The
     * default lockless path bypasses this entirely.
     */
    private _acquireLock;
    /**
     * Use instead of {@link GoTrueClient.getSession} inside the library. Loads the session
     * via `__loadSession` (which may trigger a refresh if the access token is
     * within the expiry margin) and runs `fn` with the result.
     */
    private _useSession;
    /**
     * NEVER USE DIRECTLY!
     *
     * Always use `_useSession`.
     */
    private __loadSession;
    /**
     * Gets the current user details if there is an existing session. This method
     * performs a network request to the Supabase Auth server, so the returned
     * value is authentic and can be used to base authorization rules on.
     *
     * @param jwt Takes in an optional access token JWT. If no JWT is provided, the JWT from the current session is used.
     *
     * @category Auth
     *
     * @remarks
     * - This method fetches the user object from the database instead of local session.
     * - This method is useful for checking if the user is authorized because it validates the user's access token JWT on the server.
     * - Should always be used when checking for user authorization on the server. On the client, you can instead use `getSession().session.user` for faster results. `getSession` is insecure on the server.
     *
     * @example Get the logged in user with the current existing session
     * ```js
     * const { data: { user } } = await supabase.auth.getUser()
     * ```
     *
     * @exampleResponse Get the logged in user with the current existing session
     * ```json
     * {
     *   "data": {
     *     "user": {
     *       "id": "11111111-1111-1111-1111-111111111111",
     *       "aud": "authenticated",
     *       "role": "authenticated",
     *       "email": "example@email.com",
     *       "email_confirmed_at": "2024-01-01T00:00:00Z",
     *       "phone": "",
     *       "confirmed_at": "2024-01-01T00:00:00Z",
     *       "last_sign_in_at": "2024-01-01T00:00:00Z",
     *       "app_metadata": {
     *         "provider": "email",
     *         "providers": [
     *           "email"
     *         ]
     *       },
     *       "user_metadata": {
     *         "email": "example@email.com",
     *         "email_verified": false,
     *         "phone_verified": false,
     *         "sub": "11111111-1111-1111-1111-111111111111"
     *       },
     *       "identities": [
     *         {
     *           "identity_id": "22222222-2222-2222-2222-222222222222",
     *           "id": "11111111-1111-1111-1111-111111111111",
     *           "user_id": "11111111-1111-1111-1111-111111111111",
     *           "identity_data": {
     *             "email": "example@email.com",
     *             "email_verified": false,
     *             "phone_verified": false,
     *             "sub": "11111111-1111-1111-1111-111111111111"
     *           },
     *           "provider": "email",
     *           "last_sign_in_at": "2024-01-01T00:00:00Z",
     *           "created_at": "2024-01-01T00:00:00Z",
     *           "updated_at": "2024-01-01T00:00:00Z",
     *           "email": "example@email.com"
     *         }
     *       ],
     *       "created_at": "2024-01-01T00:00:00Z",
     *       "updated_at": "2024-01-01T00:00:00Z",
     *       "is_anonymous": false
     *     }
     *   },
     *   "error": null
     * }
     * ```
     *
     * @example Get the logged in user with a custom access token jwt
     * ```js
     * const { data: { user } } = await supabase.auth.getUser(jwt)
     * ```
     */
    getUser(jwt?: string): Promise<UserResponse>;
    private _getUser;
    /**
     * Updates user data for a logged in user.
     *
     * @category Auth
     *
     * @remarks
     * - In order to use the `updateUser()` method, the user needs to be signed in first.
     * - By default, email updates sends a confirmation link to both the user's current and new email.
     * To only send a confirmation link to the user's new email, disable **Secure email change** in your project's [email auth provider settings](/dashboard/project/_/auth/providers).
     *
     * @exampleDescription Update the email for an authenticated user
     * Sends a "Confirm Email Change" email to the new address. If **Secure Email Change** is enabled (default), confirmation is also required from the **old email** before the change is applied. To skip dual confirmation and apply the change after only the new email is verified, disable **Secure Email Change** in the [Email Auth Provider settings](/dashboard/project/_/auth/providers?provider=Email).
     *
     * @example Update the email for an authenticated user
     * ```js
     * const { data, error } = await supabase.auth.updateUser({
     *   email: 'new@email.com'
     * })
     * ```
     *
     * @exampleResponse Update the email for an authenticated user
     * ```json
     * {
     *   "data": {
     *     "user": {
     *       "id": "11111111-1111-1111-1111-111111111111",
     *       "aud": "authenticated",
     *       "role": "authenticated",
     *       "email": "example@email.com",
     *       "email_confirmed_at": "2024-01-01T00:00:00Z",
     *       "phone": "",
     *       "confirmed_at": "2024-01-01T00:00:00Z",
     *       "new_email": "new@email.com",
     *       "email_change_sent_at": "2024-01-01T00:00:00Z",
     *       "last_sign_in_at": "2024-01-01T00:00:00Z",
     *       "app_metadata": {
     *         "provider": "email",
     *         "providers": [
     *           "email"
     *         ]
     *       },
     *       "user_metadata": {
     *         "email": "example@email.com",
     *         "email_verified": false,
     *         "phone_verified": false,
     *         "sub": "11111111-1111-1111-1111-111111111111"
     *       },
     *       "identities": [
     *         {
     *           "identity_id": "22222222-2222-2222-2222-222222222222",
     *           "id": "11111111-1111-1111-1111-111111111111",
     *           "user_id": "11111111-1111-1111-1111-111111111111",
     *           "identity_data": {
     *             "email": "example@email.com",
     *             "email_verified": false,
     *             "phone_verified": false,
     *             "sub": "11111111-1111-1111-1111-111111111111"
     *           },
     *           "provider": "email",
     *           "last_sign_in_at": "2024-01-01T00:00:00Z",
     *           "created_at": "2024-01-01T00:00:00Z",
     *           "updated_at": "2024-01-01T00:00:00Z",
     *           "email": "example@email.com"
     *         }
     *       ],
     *       "created_at": "2024-01-01T00:00:00Z",
     *       "updated_at": "2024-01-01T00:00:00Z",
     *       "is_anonymous": false
     *     }
     *   },
     *   "error": null
     * }
     * ```
     *
     * @exampleDescription Update the phone number for an authenticated user
     * Sends a one-time password (OTP) to the new phone number.
     *
     * @example Update the phone number for an authenticated user
     * ```js
     * const { data, error } = await supabase.auth.updateUser({
     *   phone: '123456789'
     * })
     * ```
     *
     * @example Update the password for an authenticated user
     * ```js
     * const { data, error } = await supabase.auth.updateUser({
     *   password: 'new password'
     * })
     * ```
     *
     * @exampleDescription Update the user's metadata
     * Updates the user's custom metadata.
     *
     * **Note**: The `data` field maps to the `auth.users.raw_user_meta_data` column in your Supabase database. When calling `getUser()`, the data will be available as `user.user_metadata`.
     *
     * @example Update the user's metadata
     * ```js
     * const { data, error } = await supabase.auth.updateUser({
     *   data: { hello: 'world' }
     * })
     * ```
     *
     * @exampleDescription Update the user's password with a nonce
     * If **Secure password change** is enabled in your [project's email provider settings](/dashboard/project/_/auth/providers), updating the user's password would require a nonce if the user **hasn't recently signed in**. The nonce is sent to the user's email or phone number. A user is deemed recently signed in if the session was created in the last 24 hours.
     *
     * @example Update the user's password with a nonce
     * ```js
     * const { data, error } = await supabase.auth.updateUser({
     *   password: 'new password',
     *   nonce: '123456'
     * })
     * ```
     */
    updateUser(attributes: UserAttributes, options?: {
        emailRedirectTo?: string | undefined;
    }): Promise<UserResponse>;
    protected _updateUser(attributes: UserAttributes, options?: {
        emailRedirectTo?: string | undefined;
    }): Promise<UserResponse>;
    /**
     * Sets the session data from the current session. If the current session is expired, setSession will take care of refreshing it to obtain a new session.
     * If the refresh token or access token in the current session is invalid, an error will be thrown.
     * @param currentSession The current session that minimally contains an access token and refresh token.
     *
     * @category Auth
     *
     * @remarks
     * - This method sets the session using an `access_token` and `refresh_token`.
     * - If successful, a `SIGNED_IN` event is emitted.
     *
     * @exampleDescription Set the session
     * Sets the session data from an access_token and refresh_token, then returns an auth response or error.
     *
     * @example Set the session
     * ```js
     *   const { data, error } = await supabase.auth.setSession({
     *     access_token,
     *     refresh_token
     *   })
     * ```
     *
     * @exampleResponse Set the session
     * ```json
     * {
     *   "data": {
     *     "user": {
     *       "id": "11111111-1111-1111-1111-111111111111",
     *       "aud": "authenticated",
     *       "role": "authenticated",
     *       "email": "example@email.com",
     *       "email_confirmed_at": "2024-01-01T00:00:00Z",
     *       "phone": "",
     *       "confirmed_at": "2024-01-01T00:00:00Z",
     *       "last_sign_in_at": "2024-01-01T00:00:00Z",
     *       "app_metadata": {
     *         "provider": "email",
     *         "providers": [
     *           "email"
     *         ]
     *       },
     *       "user_metadata": {
     *         "email": "example@email.com",
     *         "email_verified": false,
     *         "phone_verified": false,
     *         "sub": "11111111-1111-1111-1111-111111111111"
     *       },
     *       "identities": [
     *         {
     *           "identity_id": "22222222-2222-2222-2222-222222222222",
     *           "id": "11111111-1111-1111-1111-111111111111",
     *           "user_id": "11111111-1111-1111-1111-111111111111",
     *           "identity_data": {
     *             "email": "example@email.com",
     *             "email_verified": false,
     *             "phone_verified": false,
     *             "sub": "11111111-1111-1111-1111-111111111111"
     *           },
     *           "provider": "email",
     *           "last_sign_in_at": "2024-01-01T00:00:00Z",
     *           "created_at": "2024-01-01T00:00:00Z",
     *           "updated_at": "2024-01-01T00:00:00Z",
     *           "email": "example@email.com"
     *         }
     *       ],
     *       "created_at": "2024-01-01T00:00:00Z",
     *       "updated_at": "2024-01-01T00:00:00Z",
     *       "is_anonymous": false
     *     },
     *     "session": {
     *       "access_token": "<ACCESS_TOKEN>",
     *       "refresh_token": "<REFRESH_TOKEN>",
     *       "user": {
     *         "id": "11111111-1111-1111-1111-111111111111",
     *         "aud": "authenticated",
     *         "role": "authenticated",
     *         "email": "example@email.com",
     *         "email_confirmed_at": "2024-01-01T00:00:00Z",
     *         "phone": "",
     *         "confirmed_at": "2024-01-01T00:00:00Z",
     *         "last_sign_in_at": "11111111-1111-1111-1111-111111111111",
     *         "app_metadata": {
     *           "provider": "email",
     *           "providers": [
     *             "email"
     *           ]
     *         },
     *         "user_metadata": {
     *           "email": "example@email.com",
     *           "email_verified": false,
     *           "phone_verified": false,
     *           "sub": "11111111-1111-1111-1111-111111111111"
     *         },
     *         "identities": [
     *           {
     *             "identity_id": "2024-01-01T00:00:00Z",
     *             "id": "11111111-1111-1111-1111-111111111111",
     *             "user_id": "11111111-1111-1111-1111-111111111111",
     *             "identity_data": {
     *               "email": "example@email.com",
     *               "email_verified": false,
     *               "phone_verified": false,
     *               "sub": "11111111-1111-1111-1111-111111111111"
     *             },
     *             "provider": "email",
     *             "last_sign_in_at": "2024-01-01T00:00:00Z",
     *             "created_at": "2024-01-01T00:00:00Z",
     *             "updated_at": "2024-01-01T00:00:00Z",
     *             "email": "example@email.com"
     *           }
     *         ],
     *         "created_at": "2024-01-01T00:00:00Z",
     *         "updated_at": "2024-01-01T00:00:00Z",
     *         "is_anonymous": false
     *       },
     *       "token_type": "bearer",
     *       "expires_in": 3500,
     *       "expires_at": 1700000000
     *     }
     *   },
     *   "error": null
     * }
     * ```
     */
    setSession(currentSession: {
        access_token: string;
        refresh_token: string;
    }): Promise<AuthResponse>;
    protected _setSession(currentSession: {
        access_token: string;
        refresh_token: string;
    }): Promise<AuthResponse>;
    /**
     * Returns a new session, regardless of expiry status.
     * Takes in an optional current session. If not passed in, then refreshSession() will attempt to retrieve it from getSession().
     * If the current session's refresh token is invalid, an error will be thrown.
     * @param currentSession The current session. If passed in, it must contain a refresh token.
     *
     * @category Auth
     *
     * @remarks
     * - This method will refresh and return a new session whether the current one is expired or not.
     *
     * @example Refresh session using the current session
     * ```js
     * const { data, error } = await supabase.auth.refreshSession()
     * const { session, user } = data
     * ```
     *
     * @exampleResponse Refresh session using the current session
     * ```json
     * {
     *   "data": {
     *     "user": {
     *       "id": "11111111-1111-1111-1111-111111111111",
     *       "aud": "authenticated",
     *       "role": "authenticated",
     *       "email": "example@email.com",
     *       "email_confirmed_at": "2024-01-01T00:00:00Z",
     *       "phone": "",
     *       "confirmed_at": "2024-01-01T00:00:00Z",
     *       "last_sign_in_at": "2024-01-01T00:00:00Z",
     *       "app_metadata": {
     *         "provider": "email",
     *         "providers": [
     *           "email"
     *         ]
     *       },
     *       "user_metadata": {
     *         "email": "example@email.com",
     *         "email_verified": false,
     *         "phone_verified": false,
     *         "sub": "11111111-1111-1111-1111-111111111111"
     *       },
     *       "identities": [
     *         {
     *           "identity_id": "22222222-2222-2222-2222-222222222222",
     *           "id": "11111111-1111-1111-1111-111111111111",
     *           "user_id": "11111111-1111-1111-1111-111111111111",
     *           "identity_data": {
     *             "email": "example@email.com",
     *             "email_verified": false,
     *             "phone_verified": false,
     *             "sub": "11111111-1111-1111-1111-111111111111"
     *           },
     *           "provider": "email",
     *           "last_sign_in_at": "2024-01-01T00:00:00Z",
     *           "created_at": "2024-01-01T00:00:00Z",
     *           "updated_at": "2024-01-01T00:00:00Z",
     *           "email": "example@email.com"
     *         }
     *       ],
     *       "created_at": "2024-01-01T00:00:00Z",
     *       "updated_at": "2024-01-01T00:00:00Z",
     *       "is_anonymous": false
     *     },
     *     "session": {
     *       "access_token": "<ACCESS_TOKEN>",
     *       "token_type": "bearer",
     *       "expires_in": 3600,
     *       "expires_at": 1700000000,
     *       "refresh_token": "<REFRESH_TOKEN>",
     *       "user": {
     *         "id": "11111111-1111-1111-1111-111111111111",
     *         "aud": "authenticated",
     *         "role": "authenticated",
     *         "email": "example@email.com",
     *         "email_confirmed_at": "2024-01-01T00:00:00Z",
     *         "phone": "",
     *         "confirmed_at": "2024-01-01T00:00:00Z",
     *         "last_sign_in_at": "2024-01-01T00:00:00Z",
     *         "app_metadata": {
     *           "provider": "email",
     *           "providers": [
     *             "email"
     *           ]
     *         },
     *         "user_metadata": {
     *           "email": "example@email.com",
     *           "email_verified": false,
     *           "phone_verified": false,
     *           "sub": "11111111-1111-1111-1111-111111111111"
     *         },
     *         "identities": [
     *           {
     *             "identity_id": "22222222-2222-2222-2222-222222222222",
     *             "id": "11111111-1111-1111-1111-111111111111",
     *             "user_id": "11111111-1111-1111-1111-111111111111",
     *             "identity_data": {
     *               "email": "example@email.com",
     *               "email_verified": false,
     *               "phone_verified": false,
     *               "sub": "11111111-1111-1111-1111-111111111111"
     *             },
     *             "provider": "email",
     *             "last_sign_in_at": "2024-01-01T00:00:00Z",
     *             "created_at": "2024-01-01T00:00:00Z",
     *             "updated_at": "2024-01-01T00:00:00Z",
     *             "email": "example@email.com"
     *           }
     *         ],
     *         "created_at": "2024-01-01T00:00:00Z",
     *         "updated_at": "2024-01-01T00:00:00Z",
     *         "is_anonymous": false
     *       }
     *     }
     *   },
     *   "error": null
     * }
     * ```
     *
     * @example Refresh session using a refresh token
     * ```js
     * const { data, error } = await supabase.auth.refreshSession({ refresh_token })
     * const { session, user } = data
     * ```
     */
    refreshSession(currentSession?: {
        refresh_token: string;
    }): Promise<AuthResponse>;
    protected _refreshSession(currentSession?: {
        refresh_token: string;
    }): Promise<AuthResponse>;
    /**
     * Gets the session data from a URL string
     */
    private _getSessionFromURL;
    /**
     * Checks if the current URL contains parameters given by an implicit oauth grant flow (https://www.rfc-editor.org/rfc/rfc6749.html#section-4.2)
     *
     * If `detectSessionInUrl` is a function, it will be called with the URL and params to determine
     * if the URL should be processed as a Supabase auth callback. This allows users to exclude
     * URLs from other OAuth providers (e.g., Facebook Login) that also return access_token in the fragment.
     */
    private _isImplicitGrantCallback;
    /**
     * Checks if the current URL and backing storage contain parameters given by a PKCE flow
     */
    private _isPKCECallback;
    /**
     * Inside a browser context, `signOut()` will remove the logged in user from the browser session and log them out - removing all items from localstorage and then trigger a `"SIGNED_OUT"` event.
     *
     * For server-side management, you can revoke all refresh tokens for a user by passing a user's JWT through to `auth.api.signOut(JWT: string)`.
     * There is no way to revoke a user's access token jwt until it expires. It is recommended to set a shorter expiry on the jwt for this reason.
     *
     * If using `others` scope, no `SIGNED_OUT` event is fired!
     *
     * **Warning:** the default `scope` is `'global'`. This signs the user out of
     * **every device they are currently signed in on**, not just the current
     * tab/session. If you only want to sign the user out of the current session
     * (the behavior most other auth libraries default to), pass
     * `{ scope: 'local' }` explicitly.
     *
     * @category Auth
     *
     * @remarks
     * - In order to use the `signOut()` method, the user needs to be signed in first.
     * - By default, `signOut()` uses the **global** scope, which signs out the user
     *   on every device they are signed in on (not just the current one). Pass
     *   `{ scope: 'local' }` to only sign out the current session. This is
     *   usually what apps want on a "Sign out" button, especially when users
     *   sign in from multiple devices and do not expect signing out of one to
     *   terminate the others.
     * - Since Supabase Auth uses JWTs for authentication, the access token JWT will be valid until it's expired. When the user signs out, Supabase revokes the refresh token and deletes the JWT from the client-side. This does not revoke the JWT and it will still be valid until it expires.
     *
     * @example Sign out of every device (global – default)
     * ```js
     * const { error } = await supabase.auth.signOut()
     * ```
     *
     * @example Sign out only the current session (recommended for most apps)
     * ```js
     * const { error } = await supabase.auth.signOut({ scope: 'local' })
     * ```
     *
     * @example Sign out of all other sessions, keep the current one
     * ```js
     * const { error } = await supabase.auth.signOut({ scope: 'others' })
     * ```
     */
    signOut(options?: SignOut): Promise<{
        error: AuthError | null;
    }>;
    protected _signOut({ scope }?: SignOut): Promise<{
        error: AuthError | null;
    }>;
    /**
     * Receive a notification every time an auth event happens.
     * Safe to use without an async function as callback.
     *
     * @param callback A callback function to be invoked when an auth event happens.
     */
    onAuthStateChange(callback: (event: AuthChangeEvent, session: Session | null) => void): {
        data: {
            subscription: Subscription;
        };
    };
    /**
     * Receive a notification every time an auth event happens. Common reentry
     * patterns (`getUser`, `setSession`, reading the session from inside a
     * handler) complete normally. One hazard remains: calling `refreshSession`
     * (or anything that routes through `_callRefreshToken`) from inside a
     * `TOKEN_REFRESHED` handler. `refreshingDeferred` resolves only after
     * `_notifyAllSubscribers` returns, so the inner refresh dedupes onto the
     * outer's unresolved promise and the two wait on each other.
     *
     * @param callback A callback function to be invoked when an auth event happens.
     *
     * @deprecated Async callbacks can deadlock when they trigger a nested
     * refresh from a `TOKEN_REFRESHED` event. Prefer the sync overload, or move
     * refresh-triggering work outside the callback.
     */
    onAuthStateChange(callback: (event: AuthChangeEvent, session: Session | null) => Promise<void>): {
        data: {
            subscription: Subscription;
        };
    };
    private _emitInitialSession;
    /**
     * Sends a password reset request to an email address. This method supports the PKCE flow.
     *
     * @param email The email address of the user.
     * @param options.redirectTo The URL to send the user to after they click the password reset link.
     * @param options.captchaToken Verification token received when the user completes the captcha on the site.
     *
     * @category Auth
     *
     * @remarks
     * - The password reset flow consist of 2 broad steps: (i) Allow the user to login via the password reset link; (ii) Update the user's password.
     * - The `resetPasswordForEmail()` only sends a password reset link to the user's email.
     * To update the user's password, see [`updateUser()`](/docs/reference/javascript/auth-updateuser).
     * - A `PASSWORD_RECOVERY` event will be emitted when the password recovery link is clicked.
     * You can use [`onAuthStateChange()`](/docs/reference/javascript/auth-onauthstatechange) to listen and invoke a callback function on these events.
     * - When the user clicks the reset link in the email they are redirected back to your application.
     * You can configure the URL that the user is redirected to with the `redirectTo` parameter.
     * See [redirect URLs and wildcards](/docs/guides/auth/redirect-urls#use-wildcards-in-redirect-urls) to add additional redirect URLs to your project.
     * - After the user has been redirected successfully, prompt them for a new password and call `updateUser()`:
     * ```js
     * const { data, error } = await supabase.auth.updateUser({
     *   password: new_password
     * })
     * ```
     *
     * @example Reset password
     * ```js
     * const { data, error } = await supabase.auth.resetPasswordForEmail(email, {
     *   redirectTo: 'https://example.com/update-password',
     * })
     * ```
     *
     * @exampleResponse Reset password
     * ```json
     * {
     *   data: {}
     *   error: null
     * }
     * ```
     *
     * @example Reset password (React)
     * ```js
     * /**
     *  * Step 1: Send the user an email to get a password reset token.
     *  * This email contains a link which sends the user back to your application.
     *  *\/
     * const { data, error } = await supabase.auth
     *   .resetPasswordForEmail('user@email.com')
     *
     * /**
     *  * Step 2: Once the user is redirected back to your application,
     *  * ask the user to reset their password.
     *  *\/
     *  useEffect(() => {
     *    supabase.auth.onAuthStateChange(async (event, session) => {
     *      if (event == "PASSWORD_RECOVERY") {
     *        const newPassword = prompt("What would you like your new password to be?");
     *        const { data, error } = await supabase.auth
     *          .updateUser({ password: newPassword })
     *
     *        if (data) alert("Password updated successfully!")
     *        if (error) alert("There was an error updating your password.")
     *      }
     *    })
     *  }, [])
     * ```
     */
    resetPasswordForEmail(email: string, options?: {
        redirectTo?: string;
        captchaToken?: string;
    }): Promise<{
        data: {};
        error: null;
    } | {
        data: null;
        error: AuthError;
    }>;
    /**
     * Gets all the identities linked to a user.
     *
     * @category Auth
     *
     * @remarks
     * - The user needs to be signed in to call `getUserIdentities()`.
     *
     * @example Returns a list of identities linked to the user
     * ```js
     * const { data, error } = await supabase.auth.getUserIdentities()
     * ```
     *
     * @exampleResponse Returns a list of identities linked to the user
     * ```json
     * {
     *   "data": {
     *     "identities": [
     *       {
     *         "identity_id": "22222222-2222-2222-2222-222222222222",
     *         "id": "2024-01-01T00:00:00Z",
     *         "user_id": "2024-01-01T00:00:00Z",
     *         "identity_data": {
     *           "email": "example@email.com",
     *           "email_verified": false,
     *           "phone_verified": false,
     *           "sub": "11111111-1111-1111-1111-111111111111"
     *         },
     *         "provider": "email",
     *         "last_sign_in_at": "2024-01-01T00:00:00Z",
     *         "created_at": "2024-01-01T00:00:00Z",
     *         "updated_at": "2024-01-01T00:00:00Z",
     *         "email": "example@email.com"
     *       }
     *     ]
     *   },
     *   "error": null
     * }
     * ```
     */
    getUserIdentities(): Promise<{
        data: {
            identities: UserIdentity[];
        };
        error: null;
    } | {
        data: null;
        error: AuthError;
    }>;
    /**
     * Links an oauth identity to an existing user.
     * This method supports the PKCE flow.
     */
    linkIdentity(credentials: SignInWithOAuthCredentials): Promise<OAuthResponse>;
    /**
     * Links an OIDC identity to an existing user.
     */
    linkIdentity(credentials: SignInWithIdTokenCredentials): Promise<AuthTokenResponse>;
    private linkIdentityOAuth;
    private linkIdentityIdToken;
    /**
     * Unlinks an identity from a user by deleting it. The user will no longer be able to sign in with that identity once it's unlinked.
     *
     * @category Auth
     *
     * @remarks
     * - The **Enable Manual Linking** option must be enabled from your [project's authentication settings](/dashboard/project/_/auth/providers).
     * - The user needs to be signed in to call `unlinkIdentity()`.
     * - The user must have at least 2 identities in order to unlink an identity.
     * - The identity to be unlinked must belong to the user.
     *
     * @example Unlink an identity
     * ```js
     * // retrieve all identities linked to a user
     * const identities = await supabase.auth.getUserIdentities()
     *
     * // find the google identity
     * const googleIdentity = identities.find(
     *   identity => identity.provider === 'google'
     * )
     *
     * // unlink the google identity
     * const { error } = await supabase.auth.unlinkIdentity(googleIdentity)
     * ```
     */
    unlinkIdentity(identity: UserIdentity): Promise<{
        data: {};
        error: null;
    } | {
        data: null;
        error: AuthError;
    }>;
    /**
     * Generates a new JWT.
     * @param refreshToken A valid refresh token that was returned on login.
     */
    private _refreshAccessToken;
    private _isValidSession;
    private _handleProviderSignIn;
    /**
     * Recovers the session from LocalStorage and refreshes the token
     * Note: this method is async to accommodate for AsyncStorage e.g. in React native.
     */
    private _recoverAndRefresh;
    private _callRefreshToken;
    private _notifyAllSubscribers;
    /**
     * set currentSession and currentUser
     * process to _startAutoRefreshToken if possible
     */
    private _saveSession;
    private _removeSession;
    /**
     * Removes any registered visibilitychange callback.
     *
     * {@link GoTrueClient.startAutoRefresh}
     * {@link GoTrueClient.stopAutoRefresh}
     */
    private _removeVisibilityChangedCallback;
    /**
     * This is the private implementation of {@link GoTrueClient.startAutoRefresh}. Use this
     * within the library.
     */
    private _startAutoRefresh;
    /**
     * This is the private implementation of {@link GoTrueClient.stopAutoRefresh}. Use this
     * within the library.
     */
    private _stopAutoRefresh;
    /**
     * Starts an auto-refresh process in the background. The session is checked
     * every few seconds. Close to the time of expiration a process is started to
     * refresh the session. If refreshing fails it will be retried for as long as
     * necessary.
     *
     * If you set the {@link GoTrueClientOptions#autoRefreshToken} you don't need
     * to call this function, it will be called for you.
     *
     * On browsers the refresh process works only when the tab/window is in the
     * foreground to conserve resources as well as prevent race conditions and
     * flooding auth with requests. If you call this method any managed
     * visibility change callback will be removed and you must manage visibility
     * changes on your own.
     *
     * On non-browser platforms the refresh process works *continuously* in the
     * background, which may not be desirable. You should hook into your
     * platform's foreground indication mechanism and call these methods
     * appropriately to conserve resources.
     *
     * {@link GoTrueClient.stopAutoRefresh}
     *
     * @category Auth
     *
     * @remarks
     * - Only useful in non-browser environments such as React Native or Electron.
     * - The Supabase Auth library automatically starts and stops proactively refreshing the session when a tab is focused or not.
     * - On non-browser platforms, such as mobile or desktop apps built with web technologies, the library is not able to effectively determine whether the application is _focused_ or not.
     * - To give this hint to the application, you should be calling this method when the app is in focus and calling `supabase.auth.stopAutoRefresh()` when it's out of focus.
     *
     * @example Start and stop auto refresh in React Native
     * ```js
     * import { AppState } from 'react-native'
     *
     * // make sure you register this only once!
     * AppState.addEventListener('change', (state) => {
     *   if (state === 'active') {
     *     supabase.auth.startAutoRefresh()
     *   } else {
     *     supabase.auth.stopAutoRefresh()
     *   }
     * })
     * ```
     */
    startAutoRefresh(): Promise<void>;
    /**
     * Stops an active auto refresh process running in the background (if any).
     *
     * If you call this method any managed visibility change callback will be
     * removed and you must manage visibility changes on your own.
     *
     * See {@link GoTrueClient.startAutoRefresh} for more details.
     *
     * @category Auth
     *
     * @remarks
     * - Only useful in non-browser environments such as React Native or Electron.
     * - The Supabase Auth library automatically starts and stops proactively refreshing the session when a tab is focused or not.
     * - On non-browser platforms, such as mobile or desktop apps built with web technologies, the library is not able to effectively determine whether the application is _focused_ or not.
     * - When your application goes in the background or out of focus, call this method to stop the proactive refreshing of the session.
     *
     * @example Start and stop auto refresh in React Native
     * ```js
     * import { AppState } from 'react-native'
     *
     * // make sure you register this only once!
     * AppState.addEventListener('change', (state) => {
     *   if (state === 'active') {
     *     supabase.auth.startAutoRefresh()
     *   } else {
     *     supabase.auth.stopAutoRefresh()
     *   }
     * })
     * ```
     */
    stopAutoRefresh(): Promise<void>;
    /**
     * Tears down the client's background work: stops the auto-refresh interval,
     * removes the `visibilitychange` listener, closes the cross-tab
     * `BroadcastChannel`, and clears registered `onAuthStateChange` subscribers.
     *
     * Call this from cleanup hooks when the client is being replaced before
     * its JS realm is destroyed. React Strict Mode and HMR are the common
     * cases. Any in-flight `fetch` calls continue to completion and may still
     * write to storage; dispose doesn't abort them or erase storage.
     *
     * Lifecycle caveat: because in-flight refreshes are not aborted, a
     * disposed instance can still persist a rotated session to storage after
     * `dispose()` returns. A subsequent `createClient` against the same
     * `storageKey` will pick up that session on its next read. If you need
     * strict isolation between client lifecycles, await any pending auth
     * operation before calling `dispose()` (or change the `storageKey` for
     * the replacement client).
     *
     * Safe to call repeatedly.
     *
     * @category Auth
     *
     * @example Cleanup on React unmount
     * ```ts
     * useEffect(() => {
     *   const client = createClient(...)
     *   return () => { client.auth.dispose() }
     * }, [])
     * ```
     */
    dispose(): Promise<void>;
    /**
     * Runs the auto refresh token tick.
     */
    private _autoRefreshTokenTick;
    /**
     * Registers callbacks on the browser / platform, which in-turn run
     * algorithms when the browser window/tab are in foreground. On non-browser
     * platforms it assumes always foreground.
     */
    private _handleVisibilityChange;
    /**
     * Callback registered with `window.addEventListener('visibilitychange')`.
     */
    private _onVisibilityChanged;
    /**
     * Generates the relevant login URL for a third-party provider.
     * @param options.redirectTo A URL or mobile address to send the user to after they are confirmed.
     * @param options.scopes A space-separated list of scopes granted to the OAuth application.
     * @param options.queryParams An object of key-value pairs containing query parameters granted to the OAuth application.
     */
    private _getUrlForProvider;
    /**
     * Appends the reserved flow id parameter to a redirect URL so the callback
     * can be matched to the verifier stored for its flow. Opt-in via
     * `experimental.appendPkceFlowIdToRedirects`: redirect URLs are validated
     * against the project's allow list including the query string, so an extra
     * parameter can stop exact (non-wildcard) entries from matching.
     */
    private _maybeAppendFlowIdToRedirect;
    /**
     * Generates and stores a PKCE challenge/verifier pair for a new flow,
     * logging any pending verifier the bounded slot ring evicts.
     */
    private _getCodeChallengeAndMethod;
    private _unenroll;
    /**
     * {@link GoTrueMFAApi#enroll}
     */
    private _enroll;
    /**
     * {@link GoTrueMFAApi#verify}
     */
    private _verify;
    /**
     * {@link GoTrueMFAApi#challenge}
     */
    private _challenge;
    /**
     * {@link GoTrueMFAApi#challengeAndVerify}
     */
    private _challengeAndVerify;
    /**
     * {@link GoTrueMFAApi#listFactors}
     */
    private _listFactors;
    /**
     * {@link GoTrueMFAApi#getAuthenticatorAssuranceLevel}
     */
    private _getAuthenticatorAssuranceLevel;
    /**
     * {@link AuthMFARecoveryCodesApi#getStatus}
     */
    private _getRecoveryCodesStatus;
    /**
     * {@link AuthMFARecoveryCodesApi#generate}
     */
    private _generateRecoveryCodes;
    /**
     * {@link AuthMFARecoveryCodesApi#verify}
     */
    private _verifyRecoveryCode;
    /**
     * {@link AuthMFARecoveryCodesApi#regenerate}
     */
    private _regenerateRecoveryCodes;
    /**
     * {@link AuthMFARecoveryCodesApi#unenroll}
     */
    private _unenrollRecoveryCodes;
    /**
     * Retrieves details about an OAuth authorization request.
     * Only relevant when the OAuth 2.1 server is enabled in Supabase Auth.
     *
     * Returns authorization details including client info, scopes, and user information.
     * If the response includes only a redirect_url field, it means consent was already given - the caller
     * should handle the redirect manually if needed.
     */
    private _getAuthorizationDetails;
    /**
     * Approves an OAuth authorization request.
     * Only relevant when the OAuth 2.1 server is enabled in Supabase Auth.
     */
    private _approveAuthorization;
    /**
     * Denies an OAuth authorization request.
     * Only relevant when the OAuth 2.1 server is enabled in Supabase Auth.
     */
    private _denyAuthorization;
    /**
     * Lists all OAuth grants that the authenticated user has authorized.
     * Only relevant when the OAuth 2.1 server is enabled in Supabase Auth.
     */
    private _listOAuthGrants;
    /**
     * Revokes a user's OAuth grant for a specific client.
     * Only relevant when the OAuth 2.1 server is enabled in Supabase Auth.
     */
    private _revokeOAuthGrant;
    private fetchJwk;
    /**
     * Extracts the JWT claims present in the access token by first verifying the
     * JWT against the server's JSON Web Key Set endpoint
     * `/.well-known/jwks.json` which is often cached, resulting in significantly
     * faster responses. Prefer this method over {@link GoTrueClient.getUser} which always
     * sends a request to the Auth server for each JWT.
     *
     * If the project is not using an asymmetric JWT signing key (like ECC or
     * RSA) it always sends a request to the Auth server (similar to
     * {@link GoTrueClient.getUser}) to verify the JWT.
     *
     * @param jwt An optional specific JWT you wish to verify, not the one you
     *            can obtain from {@link GoTrueClient.getSession}.
     * @param options Various additional options that allow you to customize the
     *                behavior of this method.
     *
     * @category Auth
     *
     * @remarks
     * - Parses the user's [access token](/docs/guides/auth/sessions#access-token-jwt-claims) as a [JSON Web Token (JWT)](/docs/guides/auth/jwts) and returns its components if valid and not expired.
     * - If your project is using asymmetric JWT signing keys, then the verification is done locally usually without a network request using the [WebCrypto API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API).
     * - A network request is sent to your project's JWT signing key discovery endpoint `https://project-id.supabase.co/auth/v1/.well-known/jwks.json`, which is cached locally. If your environment is ephemeral, such as a Lambda function that is destroyed after every request, a network request will be sent for each new invocation. Supabase provides a network-edge cache providing fast responses for these situations.
     * - If the user's access token is about to expire when calling this function, the user's session will first be refreshed before validating the JWT.
     * - If your project is using a symmetric secret to sign the JWT, it always sends a request similar to `getUser()` to validate the JWT at the server before returning the decoded token. This is also used if the WebCrypto API is not available in the environment. Make sure you polyfill it in such situations.
     * - The returned claims can be customized per project using the [Custom Access Token Hook](/docs/guides/auth/auth-hooks/custom-access-token-hook).
     *
     * @example Get JWT claims, header and signature
     * ```js
     * const { data, error } = await supabase.auth.getClaims()
     * ```
     *
     * @exampleResponse Get JWT claims, header and signature
     * ```json
     * {
     *   "data": {
     *     "claims": {
     *       "aal": "aal1",
     *       "amr": [{
     *         "method": "email",
     *         "timestamp": 1715766000
     *       }],
     *       "app_metadata": {},
     *       "aud": "authenticated",
     *       "email": "example@email.com",
     *       "exp": 1715769600,
     *       "iat": 1715766000,
     *       "is_anonymous": false,
     *       "iss": "https://project-id.supabase.co/auth/v1",
     *       "phone": "+13334445555",
     *       "role": "authenticated",
     *       "session_id": "11111111-1111-1111-1111-111111111111",
     *       "sub": "11111111-1111-1111-1111-111111111111",
     *       "user_metadata": {}
     *     },
     *     "header": {
     *       "alg": "RS256",
     *       "typ": "JWT",
     *       "kid": "11111111-1111-1111-1111-111111111111"
     *     },
     *     "signature": [/** Uint8Array *\/],
     *   },
     *   "error": null
     * }
     * ```
     */
    getClaims(jwt?: string, options?: {
        /**
         * @deprecated Please use options.jwks instead.
         */
        keys?: JWK[];
        /** If set to `true` the `exp` claim will not be validated against the current time. */
        allowExpired?: boolean;
        /** If set, this JSON Web Key Set is going to have precedence over the cached value available on the server. */
        jwks?: {
            keys: JWK[];
        };
    }): Promise<{
        data: {
            claims: JwtPayload;
            header: JwtHeader;
            signature: Uint8Array;
        };
        error: null;
    } | {
        data: null;
        error: AuthError;
    } | {
        data: null;
        error: null;
    }>;
    /**
     * Sign in with a passkey. Handles the full WebAuthn ceremony:
     * 1. Fetches authentication challenge from server
     * 2. Prompts user via navigator.credentials.get()
     * 3. Verifies credential with server and creates session
     *
     * Requires `auth.experimental.passkey: true`.
     *
     * @category Auth
     */
    signInWithPasskey(credentials?: SignInWithPasskeyCredentials): Promise<AuthPasskeyAuthenticationVerifyResponse>;
    /**
     * Register a passkey for the current authenticated user. Handles the full WebAuthn ceremony:
     * 1. Fetches registration challenge from server
     * 2. Prompts user via navigator.credentials.create()
     * 3. Verifies credential with server
     *
     * Requires an active session. Requires `auth.experimental.passkey: true`.
     *
     * @category Auth
     */
    registerPasskey(credentials?: RegisterPasskeyCredentials): Promise<AuthPasskeyRegistrationVerifyResponse>;
    /**
     * Start passkey registration for the current authenticated user.
     * Returns WebAuthn credential creation options to pass to navigator.credentials.create().
     */
    private _startPasskeyRegistration;
    /**
     * Verify passkey registration with the credential response.
     * The credentialResponse should be the serialized output of navigator.credentials.create().
     */
    private _verifyPasskeyRegistration;
    /**
     * Start passkey authentication.
     * Returns WebAuthn credential request options to pass to navigator.credentials.get().
     */
    private _startPasskeyAuthentication;
    /**
     * Verify passkey authentication and create a session.
     * The credential should be the serialized output of navigator.credentials.get().
     */
    private _verifyPasskeyAuthentication;
    /**
     * List all passkeys for the current user.
     */
    private _listPasskeys;
    /**
     * Update a passkey.
     */
    private _updatePasskey;
    /**
     * Delete a passkey.
     */
    private _deletePasskey;
}
//# sourceMappingURL=GoTrueClient.d.ts.map