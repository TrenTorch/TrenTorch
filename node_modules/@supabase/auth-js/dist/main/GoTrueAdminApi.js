"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const fetch_1 = require("./lib/fetch");
const helpers_1 = require("./lib/helpers");
const types_1 = require("./lib/types");
const errors_1 = require("./lib/errors");
class GoTrueAdminApi {
    /**
     * Creates an admin API client that can be used to manage users and OAuth clients.
     *
     * @example Using supabase-js (recommended)
     * ```ts
     * import { createClient } from '@supabase/supabase-js'
     *
     * const supabase = createClient('https://xyzcompany.supabase.co', 'your-secret-key')
     * const { data, error } = await supabase.auth.admin.listUsers()
     * ```
     *
     * @example Standalone import for bundle-sensitive environments
     * ```ts
     * import { GoTrueAdminApi } from '@supabase/auth-js'
     *
     * const admin = new GoTrueAdminApi({
     *   url: 'https://xyzcompany.supabase.co/auth/v1',
     *   headers: { Authorization: `Bearer ${process.env.SUPABASE_SECRET_KEY}` },
     * })
     * ```
     */
    constructor({ url = '', headers = {}, fetch, experimental, }) {
        this.url = url;
        this.headers = headers;
        this.fetch = (0, helpers_1.resolveFetch)(fetch);
        this.experimental = experimental !== null && experimental !== void 0 ? experimental : {};
        this.mfa = {
            listFactors: this._listFactors.bind(this),
            deleteFactor: this._deleteFactor.bind(this),
        };
        this.oauth = {
            listClients: this._listOAuthClients.bind(this),
            createClient: this._createOAuthClient.bind(this),
            getClient: this._getOAuthClient.bind(this),
            updateClient: this._updateOAuthClient.bind(this),
            deleteClient: this._deleteOAuthClient.bind(this),
            regenerateClientSecret: this._regenerateOAuthClientSecret.bind(this),
        };
        this.customProviders = {
            listProviders: this._listCustomProviders.bind(this),
            createProvider: this._createCustomProvider.bind(this),
            getProvider: this._getCustomProvider.bind(this),
            updateProvider: this._updateCustomProvider.bind(this),
            deleteProvider: this._deleteCustomProvider.bind(this),
        };
        this.passkey = {
            listPasskeys: this._adminListPasskeys.bind(this),
            deletePasskey: this._adminDeletePasskey.bind(this),
        };
    }
    /**
     * Removes a logged-in session.
     * @param jwt A valid, logged-in JWT.
     * @param scope The logout sope.
     *
     * @category Auth
     * @subcategory Auth Admin
     */
    async signOut(jwt, scope = types_1.SIGN_OUT_SCOPES[0]) {
        if (types_1.SIGN_OUT_SCOPES.indexOf(scope) < 0) {
            throw new Error(`@supabase/auth-js: Parameter scope must be one of ${types_1.SIGN_OUT_SCOPES.join(', ')}`);
        }
        try {
            await (0, fetch_1._request)(this.fetch, 'POST', `${this.url}/logout?scope=${scope}`, {
                headers: this.headers,
                jwt,
                noResolveJson: true,
            });
            return { data: null, error: null };
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: null, error };
            }
            throw error;
        }
    }
    /**
     * Sends an invite link to an email address.
     * @param email The email address of the user.
     * @param options Additional options to be included when inviting.
     *
     * @category Auth
     * @subcategory Auth Admin
     *
     * @remarks
     * - Sends an invite link to the user's email address.
     * - The `inviteUserByEmail()` method is typically used by administrators to invite users to join the application.
     * - Note that PKCE is not supported when using `inviteUserByEmail`. This is because the browser initiating the invite is often different from the browser accepting the invite which makes it difficult to provide the security guarantees required of the PKCE flow.
     *
     * @example Invite a user
     * ```js
     * const { data, error } = await supabase.auth.admin.inviteUserByEmail('email@example.com')
     * ```
     *
     * @exampleResponse Invite a user
     * ```json
     * {
     *   "data": {
     *     "user": {
     *       "id": "11111111-1111-1111-1111-111111111111",
     *       "aud": "authenticated",
     *       "role": "authenticated",
     *       "email": "example@email.com",
     *       "invited_at": "2024-01-01T00:00:00Z",
     *       "phone": "",
     *       "confirmation_sent_at": "2024-01-01T00:00:00Z",
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
     *       "updated_at": "2024-01-01T00:00:00Z",
     *       "is_anonymous": false
     *     }
     *   },
     *   "error": null
     * }
     * ```
     */
    async inviteUserByEmail(email, options = {}) {
        try {
            return await (0, fetch_1._request)(this.fetch, 'POST', `${this.url}/invite`, {
                body: { email, data: options.data },
                headers: this.headers,
                redirectTo: options.redirectTo,
                xform: fetch_1._userResponse,
            });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: { user: null }, error };
            }
            throw error;
        }
    }
    /**
     * Generates email links and OTPs to be sent via a custom email provider.
     * @param params The parameters for generating the link, including the link `type`, the user's `email`, and type-specific options such as `password`, `data`, and `redirectTo`.
     *
     * @category Auth
     * @subcategory Auth Admin
     *
     * @remarks
     * - The following types can be passed into `generateLink()`: `signup`, `magiclink`, `invite`, `recovery`, `email_change_current`, `email_change_new`, `phone_change`.
     * - `generateLink()` only generates the email link for `email_change_email` if the **Secure email change** is enabled in your project's [email auth provider settings](/dashboard/project/_/auth/providers).
     * - `generateLink()` handles the creation of the user for `signup`, `invite` and `magiclink`.
     *
     * @example Generate a signup link
     * ```js
     * const { data, error } = await supabase.auth.admin.generateLink({
     *   type: 'signup',
     *   email: 'email@example.com',
     *   password: 'secret'
     * })
     * ```
     *
     * @exampleResponse Generate a signup link
     * ```json
     * {
     *   "data": {
     *     "properties": {
     *       "action_link": "<LINK_TO_SEND_TO_USER>",
     *       "email_otp": "999999",
     *       "hashed_token": "<HASHED_TOKEN",
     *       "redirect_to": "<REDIRECT_URL>",
     *       "verification_type": "signup"
     *     },
     *     "user": {
     *       "id": "11111111-1111-1111-1111-111111111111",
     *       "aud": "authenticated",
     *       "role": "authenticated",
     *       "email": "email@example.com",
     *       "phone": "",
     *       "confirmation_sent_at": "2024-01-01T00:00:00Z",
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
     *             "email": "email@example.com",
     *             "email_verified": false,
     *             "phone_verified": false,
     *             "sub": "11111111-1111-1111-1111-111111111111"
     *           },
     *           "provider": "email",
     *           "last_sign_in_at": "2024-01-01T00:00:00Z",
     *           "created_at": "2024-01-01T00:00:00Z",
     *           "updated_at": "2024-01-01T00:00:00Z",
     *           "email": "email@example.com"
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
     * @example Generate an invite link
     * ```js
     * const { data, error } = await supabase.auth.admin.generateLink({
     *   type: 'invite',
     *   email: 'email@example.com'
     * })
     * ```
     *
     * @example Generate a magic link
     * ```js
     * const { data, error } = await supabase.auth.admin.generateLink({
     *   type: 'magiclink',
     *   email: 'email@example.com'
     * })
     * ```
     *
     * @example Generate a recovery link
     * ```js
     * const { data, error } = await supabase.auth.admin.generateLink({
     *   type: 'recovery',
     *   email: 'email@example.com'
     * })
     * ```
     *
     * @example Generate links to change current email address
     * ```js
     * // generate an email change link to be sent to the current email address
     * const { data, error } = await supabase.auth.admin.generateLink({
     *   type: 'email_change_current',
     *   email: 'current.email@example.com',
     *   newEmail: 'new.email@example.com'
     * })
     *
     * // generate an email change link to be sent to the new email address
     * const { data, error } = await supabase.auth.admin.generateLink({
     *   type: 'email_change_new',
     *   email: 'current.email@example.com',
     *   newEmail: 'new.email@example.com'
     * })
     * ```
     */
    async generateLink(params) {
        try {
            const { options } = params, rest = tslib_1.__rest(params, ["options"]);
            const body = Object.assign(Object.assign({}, rest), options);
            if ('newEmail' in rest) {
                // replace newEmail with new_email in request body
                body.new_email = rest === null || rest === void 0 ? void 0 : rest.newEmail;
                delete body['newEmail'];
            }
            return await (0, fetch_1._request)(this.fetch, 'POST', `${this.url}/admin/generate_link`, {
                body: body,
                headers: this.headers,
                xform: fetch_1._generateLinkResponse,
                redirectTo: options === null || options === void 0 ? void 0 : options.redirectTo,
            });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return {
                    data: {
                        properties: null,
                        user: null,
                    },
                    error,
                };
            }
            throw error;
        }
    }
    // User Admin API
    /**
     * Creates a new user.
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     *
     * @category Auth
     * @subcategory Auth Admin
     *
     * @remarks
     * - To confirm the user's email address or phone number, set `email_confirm` or `phone_confirm` to true. Both arguments default to false.
     * - `createUser()` will not send a confirmation email to the user. You can use [`inviteUserByEmail()`](/docs/reference/javascript/auth-admin-inviteuserbyemail) if you want to send them an email invite instead.
     * - If you are sure that the created user's email or phone number is legitimate and verified, you can set the `email_confirm` or `phone_confirm` param to `true`.
     *
     * @example With custom user metadata
     * ```js
     * const { data, error } = await supabase.auth.admin.createUser({
     *   email: 'user@email.com',
     *   password: 'password',
     *   user_metadata: { name: 'Yoda' }
     * })
     * ```
     *
     * @exampleResponse With custom user metadata
     * ```json
     * {
     *   data: {
     *     user: {
     *       id: '1',
     *       aud: 'authenticated',
     *       role: 'authenticated',
     *       email: 'example@email.com',
     *       email_confirmed_at: '2024-01-01T00:00:00Z',
     *       phone: '',
     *       confirmation_sent_at: '2024-01-01T00:00:00Z',
     *       confirmed_at: '2024-01-01T00:00:00Z',
     *       last_sign_in_at: '2024-01-01T00:00:00Z',
     *       app_metadata: {},
     *       user_metadata: {},
     *       identities: [
     *         {
     *           "identity_id": "22222222-2222-2222-2222-222222222222",
     *           "id": "1",
     *           "user_id": "1",
     *           "identity_data": {
     *             "email": "example@email.com",
     *             "email_verified": true,
     *             "phone_verified": false,
     *             "sub": "1"
     *           },
     *           "provider": "email",
     *           "last_sign_in_at": "2024-01-01T00:00:00Z",
     *           "created_at": "2024-01-01T00:00:00Z",
     *           "updated_at": "2024-01-01T00:00:00Z",
     *           "email": "email@example.com"
     *         },
     *       ],
     *       created_at: '2024-01-01T00:00:00Z',
     *       updated_at: '2024-01-01T00:00:00Z',
     *       is_anonymous: false,
     *     }
     *   }
     *   error: null
     * }
     * ```
     *
     * @example Auto-confirm the user's email
     * ```js
     * const { data, error } = await supabase.auth.admin.createUser({
     *   email: 'user@email.com',
     *   email_confirm: true
     * })
     * ```
     *
     * @example Auto-confirm the user's phone number
     * ```js
     * const { data, error } = await supabase.auth.admin.createUser({
     *   phone: '1234567890',
     *   phone_confirm: true
     * })
     * ```
     */
    async createUser(attributes) {
        try {
            return await (0, fetch_1._request)(this.fetch, 'POST', `${this.url}/admin/users`, {
                body: attributes,
                headers: this.headers,
                xform: fetch_1._userResponse,
            });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: { user: null }, error };
            }
            throw error;
        }
    }
    /**
     * Get a list of users.
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     * @param params An object which supports `page` and `perPage` as numbers, to alter the paginated results.
     *
     * @category Auth
     * @subcategory Auth Admin
     *
     * @remarks
     * - Defaults to return 50 users per page.
     *
     * @example Get a page of users
     * ```js
     * const { data: { users }, error } = await supabase.auth.admin.listUsers()
     * ```
     *
     * @example Paginated list of users
     * ```js
     * const { data: { users }, error } = await supabase.auth.admin.listUsers({
     *   page: 1,
     *   perPage: 1000
     * })
     * ```
     */
    async listUsers(params) {
        var _a, _b, _c, _d, _e, _f, _g;
        try {
            const pagination = { nextPage: null, lastPage: 0, total: 0 };
            const response = await (0, fetch_1._request)(this.fetch, 'GET', `${this.url}/admin/users`, {
                headers: this.headers,
                noResolveJson: true,
                query: {
                    page: (_b = (_a = params === null || params === void 0 ? void 0 : params.page) === null || _a === void 0 ? void 0 : _a.toString()) !== null && _b !== void 0 ? _b : '',
                    per_page: (_d = (_c = params === null || params === void 0 ? void 0 : params.perPage) === null || _c === void 0 ? void 0 : _c.toString()) !== null && _d !== void 0 ? _d : '',
                },
                xform: fetch_1._noResolveJsonResponse,
            });
            if (response.error)
                throw response.error;
            const users = await response.json();
            const total = (_e = response.headers.get('x-total-count')) !== null && _e !== void 0 ? _e : 0;
            const links = (_g = (_f = response.headers.get('link')) === null || _f === void 0 ? void 0 : _f.split(',')) !== null && _g !== void 0 ? _g : [];
            if (links.length > 0) {
                links.forEach((link) => {
                    const page = parseInt(link.split(';')[0].split('=')[1].substring(0, 1));
                    const rel = JSON.parse(link.split(';')[1].split('=')[1]);
                    pagination[`${rel}Page`] = page;
                });
                pagination.total = parseInt(total);
            }
            return { data: Object.assign(Object.assign({}, users), pagination), error: null };
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: { users: [] }, error };
            }
            throw error;
        }
    }
    /**
     * Get user by id.
     *
     * @param uid The user's unique identifier
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     *
     * @category Auth
     * @subcategory Auth Admin
     *
     * @remarks
     * - Fetches the user object from the database based on the user's id.
     * - The `getUserById()` method requires the user's id which maps to the `auth.users.id` column.
     *
     * @example Fetch the user object using the access_token jwt
     * ```js
     * const { data, error } = await supabase.auth.admin.getUserById(1)
     * ```
     *
     * @exampleResponse Fetch the user object using the access_token jwt
     * ```json
     * {
     *   data: {
     *     user: {
     *       id: '1',
     *       aud: 'authenticated',
     *       role: 'authenticated',
     *       email: 'example@email.com',
     *       email_confirmed_at: '2024-01-01T00:00:00Z',
     *       phone: '',
     *       confirmation_sent_at: '2024-01-01T00:00:00Z',
     *       confirmed_at: '2024-01-01T00:00:00Z',
     *       last_sign_in_at: '2024-01-01T00:00:00Z',
     *       app_metadata: {},
     *       user_metadata: {},
     *       identities: [
     *         {
     *           "identity_id": "22222222-2222-2222-2222-222222222222",
     *           "id": "1",
     *           "user_id": "1",
     *           "identity_data": {
     *             "email": "example@email.com",
     *             "email_verified": true,
     *             "phone_verified": false,
     *             "sub": "1"
     *           },
     *           "provider": "email",
     *           "last_sign_in_at": "2024-01-01T00:00:00Z",
     *           "created_at": "2024-01-01T00:00:00Z",
     *           "updated_at": "2024-01-01T00:00:00Z",
     *           "email": "email@example.com"
     *         },
     *       ],
     *       created_at: '2024-01-01T00:00:00Z',
     *       updated_at: '2024-01-01T00:00:00Z',
     *       is_anonymous: false,
     *     }
     *   }
     *   error: null
     * }
     * ```
     */
    async getUserById(uid) {
        (0, helpers_1.validateUUID)(uid);
        try {
            return await (0, fetch_1._request)(this.fetch, 'GET', `${this.url}/admin/users/${uid}`, {
                headers: this.headers,
                xform: fetch_1._userResponse,
            });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: { user: null }, error };
            }
            throw error;
        }
    }
    /**
     * Updates the user data. Changes are applied directly without confirmation flows.
     *
     * @param uid The user's unique identifier
     * @param attributes The data you want to update.
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     *
     * @remarks
     * **Important:** This is a server-side operation and does **not** trigger client-side
     * `onAuthStateChange` listeners. The admin API has no connection to client state.
     *
     * To sync changes to the client after calling this method:
     * 1. On the client, call `supabase.auth.refreshSession()` to fetch the updated user data
     * 2. This will trigger the `TOKEN_REFRESHED` event and notify all listeners
     *
     * @example
     * ```typescript
     * // Server-side (Edge Function)
     * const { data, error } = await supabase.auth.admin.updateUserById(
     *   userId,
     *   { user_metadata: { preferences: { theme: 'dark' } } }
     * )
     *
     * // Client-side (to sync the changes)
     * const { data, error } = await supabase.auth.refreshSession()
     * // onAuthStateChange listeners will now be notified with updated user
     * ```
     *
     * @see {@link GoTrueClient.refreshSession} for syncing admin changes to the client
     * @see {@link GoTrueClient.updateUser} for client-side user updates (triggers listeners automatically)
     *
     * @category Auth
     * @subcategory Auth Admin
     *
     * @example Updates a user's email
     * ```js
     * const { data: user, error } = await supabase.auth.admin.updateUserById(
     *   '11111111-1111-1111-1111-111111111111',
     *   { email: 'new@email.com' }
     * )
     * ```
     *
     * @exampleResponse Updates a user's email
     * ```json
     * {
     *   "data": {
     *     "user": {
     *       "id": "11111111-1111-1111-1111-111111111111",
     *       "aud": "authenticated",
     *       "role": "authenticated",
     *       "email": "new@email.com",
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
     *     }
     *   },
     *   "error": null
     * }
     * ```
     *
     * @example Updates a user's password
     * ```js
     * const { data: user, error } = await supabase.auth.admin.updateUserById(
     *   '6aa5d0d4-2a9f-4483-b6c8-0cf4c6c98ac4',
     *   { password: 'new_password' }
     * )
     * ```
     *
     * @example Updates a user's metadata
     * ```js
     * const { data: user, error } = await supabase.auth.admin.updateUserById(
     *   '6aa5d0d4-2a9f-4483-b6c8-0cf4c6c98ac4',
     *   { user_metadata: { hello: 'world' } }
     * )
     * ```
     *
     * @example Updates a user's app_metadata
     * ```js
     * const { data: user, error } = await supabase.auth.admin.updateUserById(
     *   '6aa5d0d4-2a9f-4483-b6c8-0cf4c6c98ac4',
     *   { app_metadata: { plan: 'trial' } }
     * )
     * ```
     *
     * @example Confirms a user's email address
     * ```js
     * const { data: user, error } = await supabase.auth.admin.updateUserById(
     *   '6aa5d0d4-2a9f-4483-b6c8-0cf4c6c98ac4',
     *   { email_confirm: true }
     * )
     * ```
     *
     * @example Confirms a user's phone number
     * ```js
     * const { data: user, error } = await supabase.auth.admin.updateUserById(
     *   '6aa5d0d4-2a9f-4483-b6c8-0cf4c6c98ac4',
     *   { phone_confirm: true }
     * )
     * ```
     *
     * @example Ban a user for 100 years
     * ```js
     * const { data: user, error } = await supabase.auth.admin.updateUserById(
     *   '6aa5d0d4-2a9f-4483-b6c8-0cf4c6c98ac4',
     *   { ban_duration: '876000h' }
     * )
     * ```
     */
    async updateUserById(uid, attributes) {
        (0, helpers_1.validateUUID)(uid);
        try {
            return await (0, fetch_1._request)(this.fetch, 'PUT', `${this.url}/admin/users/${uid}`, {
                body: attributes,
                headers: this.headers,
                xform: fetch_1._userResponse,
            });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: { user: null }, error };
            }
            throw error;
        }
    }
    /**
     * Delete a user. Requires a `service_role` key.
     *
     * @param id The user id you want to remove.
     * @param shouldSoftDelete If true, then the user will be soft-deleted from the auth schema. Soft deletion allows user identification from the hashed user ID but is not reversible.
     * Defaults to false for backward compatibility.
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     *
     * @category Auth
     * @subcategory Auth Admin
     *
     * @remarks
     * - The `deleteUser()` method requires the user's ID, which maps to the `auth.users.id` column.
     *
     * @example Removes a user
     * ```js
     * const { data, error } = await supabase.auth.admin.deleteUser(
     *   '715ed5db-f090-4b8c-a067-640ecee36aa0'
     * )
     * ```
     *
     * @exampleResponse Removes a user
     * ```json
     * {
     *   "data": {
     *     "user": {}
     *   },
     *   "error": null
     * }
     * ```
     */
    async deleteUser(id, shouldSoftDelete = false) {
        (0, helpers_1.validateUUID)(id);
        try {
            return await (0, fetch_1._request)(this.fetch, 'DELETE', `${this.url}/admin/users/${id}`, {
                headers: this.headers,
                body: {
                    should_soft_delete: shouldSoftDelete,
                },
                xform: fetch_1._userResponse,
            });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: { user: null }, error };
            }
            throw error;
        }
    }
    async _listFactors(params) {
        (0, helpers_1.validateUUID)(params.userId);
        try {
            const { data, error } = await (0, fetch_1._request)(this.fetch, 'GET', `${this.url}/admin/users/${params.userId}/factors`, {
                headers: this.headers,
                xform: (factors) => {
                    return { data: { factors }, error: null };
                },
            });
            return { data, error };
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: null, error };
            }
            throw error;
        }
    }
    async _deleteFactor(params) {
        (0, helpers_1.validateUUID)(params.userId);
        (0, helpers_1.validateUUID)(params.id);
        try {
            const data = await (0, fetch_1._request)(this.fetch, 'DELETE', `${this.url}/admin/users/${params.userId}/factors/${params.id}`, {
                headers: this.headers,
            });
            return { data, error: null };
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: null, error };
            }
            throw error;
        }
    }
    /**
     * Lists all OAuth clients with optional pagination.
     * Only relevant when the OAuth 2.1 server is enabled in Supabase Auth.
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     */
    async _listOAuthClients(params) {
        var _a, _b, _c, _d, _e, _f, _g;
        try {
            const pagination = { nextPage: null, lastPage: 0, total: 0 };
            const response = await (0, fetch_1._request)(this.fetch, 'GET', `${this.url}/admin/oauth/clients`, {
                headers: this.headers,
                noResolveJson: true,
                query: {
                    page: (_b = (_a = params === null || params === void 0 ? void 0 : params.page) === null || _a === void 0 ? void 0 : _a.toString()) !== null && _b !== void 0 ? _b : '',
                    per_page: (_d = (_c = params === null || params === void 0 ? void 0 : params.perPage) === null || _c === void 0 ? void 0 : _c.toString()) !== null && _d !== void 0 ? _d : '',
                },
                xform: fetch_1._noResolveJsonResponse,
            });
            if (response.error)
                throw response.error;
            const clients = await response.json();
            const total = (_e = response.headers.get('x-total-count')) !== null && _e !== void 0 ? _e : 0;
            const links = (_g = (_f = response.headers.get('link')) === null || _f === void 0 ? void 0 : _f.split(',')) !== null && _g !== void 0 ? _g : [];
            if (links.length > 0) {
                links.forEach((link) => {
                    const page = parseInt(link.split(';')[0].split('=')[1].substring(0, 1));
                    const rel = JSON.parse(link.split(';')[1].split('=')[1]);
                    pagination[`${rel}Page`] = page;
                });
                pagination.total = parseInt(total);
            }
            return { data: Object.assign(Object.assign({}, clients), pagination), error: null };
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: { clients: [] }, error };
            }
            throw error;
        }
    }
    /**
     * Creates a new OAuth client.
     * Only relevant when the OAuth 2.1 server is enabled in Supabase Auth.
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     */
    async _createOAuthClient(params) {
        try {
            return await (0, fetch_1._request)(this.fetch, 'POST', `${this.url}/admin/oauth/clients`, {
                body: params,
                headers: this.headers,
                xform: (client) => {
                    return { data: client, error: null };
                },
            });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: null, error };
            }
            throw error;
        }
    }
    /**
     * Gets details of a specific OAuth client.
     * Only relevant when the OAuth 2.1 server is enabled in Supabase Auth.
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     */
    async _getOAuthClient(clientId) {
        try {
            return await (0, fetch_1._request)(this.fetch, 'GET', `${this.url}/admin/oauth/clients/${clientId}`, {
                headers: this.headers,
                xform: (client) => {
                    return { data: client, error: null };
                },
            });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: null, error };
            }
            throw error;
        }
    }
    /**
     * Updates an existing OAuth client.
     * Only relevant when the OAuth 2.1 server is enabled in Supabase Auth.
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     */
    async _updateOAuthClient(clientId, params) {
        try {
            return await (0, fetch_1._request)(this.fetch, 'PUT', `${this.url}/admin/oauth/clients/${clientId}`, {
                body: params,
                headers: this.headers,
                xform: (client) => {
                    return { data: client, error: null };
                },
            });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: null, error };
            }
            throw error;
        }
    }
    /**
     * Deletes an OAuth client.
     * Only relevant when the OAuth 2.1 server is enabled in Supabase Auth.
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     */
    async _deleteOAuthClient(clientId) {
        try {
            await (0, fetch_1._request)(this.fetch, 'DELETE', `${this.url}/admin/oauth/clients/${clientId}`, {
                headers: this.headers,
                noResolveJson: true,
            });
            return { data: null, error: null };
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: null, error };
            }
            throw error;
        }
    }
    /**
     * Regenerates the secret for an OAuth client.
     * Only relevant when the OAuth 2.1 server is enabled in Supabase Auth.
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     */
    async _regenerateOAuthClientSecret(clientId) {
        try {
            return await (0, fetch_1._request)(this.fetch, 'POST', `${this.url}/admin/oauth/clients/${clientId}/regenerate_secret`, {
                headers: this.headers,
                xform: (client) => {
                    return { data: client, error: null };
                },
            });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: null, error };
            }
            throw error;
        }
    }
    /**
     * Lists all custom providers with optional type filter.
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     */
    async _listCustomProviders(params) {
        try {
            const query = {};
            if (params === null || params === void 0 ? void 0 : params.type) {
                query.type = params.type;
            }
            return await (0, fetch_1._request)(this.fetch, 'GET', `${this.url}/admin/custom-providers`, {
                headers: this.headers,
                query,
                xform: (data) => {
                    var _a;
                    return { data: { providers: (_a = data === null || data === void 0 ? void 0 : data.providers) !== null && _a !== void 0 ? _a : [] }, error: null };
                },
            });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: { providers: [] }, error };
            }
            throw error;
        }
    }
    /**
     * Creates a new custom OIDC/OAuth provider.
     *
     * For OIDC providers, the server fetches and validates the OpenID Connect discovery document
     * from the issuer's well-known endpoint (or the provided `discovery_url`) at creation time.
     * This may return a validation error (`error_code: "validation_failed"`) if the discovery
     * document is unreachable, not valid JSON, missing required fields, or if the issuer
     * in the document does not match the expected issuer.
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     */
    async _createCustomProvider(params) {
        try {
            return await (0, fetch_1._request)(this.fetch, 'POST', `${this.url}/admin/custom-providers`, {
                body: params,
                headers: this.headers,
                xform: (provider) => {
                    return { data: provider, error: null };
                },
            });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: null, error };
            }
            throw error;
        }
    }
    /**
     * Gets details of a specific custom provider by identifier.
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     */
    async _getCustomProvider(identifier) {
        try {
            return await (0, fetch_1._request)(this.fetch, 'GET', `${this.url}/admin/custom-providers/${identifier}`, {
                headers: this.headers,
                xform: (provider) => {
                    return { data: provider, error: null };
                },
            });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: null, error };
            }
            throw error;
        }
    }
    /**
     * Updates an existing custom provider.
     *
     * When `issuer` or `discovery_url` is changed on an OIDC provider, the server re-fetches and
     * validates the discovery document before persisting. This may return a validation error
     * (`error_code: "validation_failed"`) if the discovery document is unreachable, invalid, or
     * the issuer does not match.
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     */
    async _updateCustomProvider(identifier, params) {
        try {
            return await (0, fetch_1._request)(this.fetch, 'PUT', `${this.url}/admin/custom-providers/${identifier}`, {
                body: params,
                headers: this.headers,
                xform: (provider) => {
                    return { data: provider, error: null };
                },
            });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: null, error };
            }
            throw error;
        }
    }
    /**
     * Deletes a custom provider.
     *
     * This function should only be called on a server. Never expose your `service_role` key in the browser.
     */
    async _deleteCustomProvider(identifier) {
        try {
            await (0, fetch_1._request)(this.fetch, 'DELETE', `${this.url}/admin/custom-providers/${identifier}`, {
                headers: this.headers,
                noResolveJson: true,
            });
            return { data: null, error: null };
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: null, error };
            }
            throw error;
        }
    }
    /**
     * Lists all passkeys for a user.
     *
     * This function should only be called on a server. Never expose your secret key in the browser.
     *
     * Requires `auth.experimental.passkey: true`.
     */
    async _adminListPasskeys(params) {
        (0, helpers_1.assertPasskeyExperimentalEnabled)(this.experimental);
        (0, helpers_1.validateUUID)(params.userId);
        try {
            return await (0, fetch_1._request)(this.fetch, 'GET', `${this.url}/admin/users/${params.userId}/passkeys`, { headers: this.headers, xform: (data) => ({ data, error: null }) });
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: null, error };
            }
            throw error;
        }
    }
    /**
     * Deletes a user's passkey.
     *
     * This function should only be called on a server. Never expose your secret key in the browser.
     *
     * Requires `auth.experimental.passkey: true`.
     */
    async _adminDeletePasskey(params) {
        (0, helpers_1.assertPasskeyExperimentalEnabled)(this.experimental);
        (0, helpers_1.validateUUID)(params.userId);
        (0, helpers_1.validateUUID)(params.passkeyId);
        try {
            await (0, fetch_1._request)(this.fetch, 'DELETE', `${this.url}/admin/users/${params.userId}/passkeys/${params.passkeyId}`, { headers: this.headers, noResolveJson: true });
            return { data: null, error: null };
        }
        catch (error) {
            if ((0, errors_1.isAuthError)(error)) {
                return { data: null, error };
            }
            throw error;
        }
    }
}
exports.default = GoTrueAdminApi;
//# sourceMappingURL=GoTrueAdminApi.js.map