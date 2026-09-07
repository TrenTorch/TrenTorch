"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.REALTIME_CHANNEL_STATES = exports.REALTIME_SUBSCRIBE_STATES = exports.REALTIME_LISTEN_TYPES = exports.REALTIME_POSTGRES_CHANGES_LISTEN_EVENT = exports.postgresChangesFilter = exports.RealtimePostgresFilterBuilder = void 0;
const tslib_1 = require("tslib");
const constants_1 = require("./lib/constants");
const RealtimePresence_1 = tslib_1.__importDefault(require("./RealtimePresence"));
const Transformers = tslib_1.__importStar(require("./lib/transformers"));
const transformers_1 = require("./lib/transformers");
const normalizeChannelError_1 = require("./lib/normalizeChannelError");
const channelAdapter_1 = tslib_1.__importDefault(require("./phoenix/channelAdapter"));
const RealtimePostgresFilterBuilder_1 = require("./RealtimePostgresFilterBuilder");
var RealtimePostgresFilterBuilder_2 = require("./RealtimePostgresFilterBuilder");
Object.defineProperty(exports, "RealtimePostgresFilterBuilder", { enumerable: true, get: function () { return RealtimePostgresFilterBuilder_2.RealtimePostgresFilterBuilder; } });
Object.defineProperty(exports, "postgresChangesFilter", { enumerable: true, get: function () { return RealtimePostgresFilterBuilder_2.postgresChangesFilter; } });
var REALTIME_POSTGRES_CHANGES_LISTEN_EVENT;
(function (REALTIME_POSTGRES_CHANGES_LISTEN_EVENT) {
    REALTIME_POSTGRES_CHANGES_LISTEN_EVENT["ALL"] = "*";
    REALTIME_POSTGRES_CHANGES_LISTEN_EVENT["INSERT"] = "INSERT";
    REALTIME_POSTGRES_CHANGES_LISTEN_EVENT["UPDATE"] = "UPDATE";
    REALTIME_POSTGRES_CHANGES_LISTEN_EVENT["DELETE"] = "DELETE";
})(REALTIME_POSTGRES_CHANGES_LISTEN_EVENT || (exports.REALTIME_POSTGRES_CHANGES_LISTEN_EVENT = REALTIME_POSTGRES_CHANGES_LISTEN_EVENT = {}));
var REALTIME_LISTEN_TYPES;
(function (REALTIME_LISTEN_TYPES) {
    REALTIME_LISTEN_TYPES["BROADCAST"] = "broadcast";
    REALTIME_LISTEN_TYPES["PRESENCE"] = "presence";
    REALTIME_LISTEN_TYPES["POSTGRES_CHANGES"] = "postgres_changes";
    REALTIME_LISTEN_TYPES["SYSTEM"] = "system";
})(REALTIME_LISTEN_TYPES || (exports.REALTIME_LISTEN_TYPES = REALTIME_LISTEN_TYPES = {}));
var REALTIME_SUBSCRIBE_STATES;
(function (REALTIME_SUBSCRIBE_STATES) {
    REALTIME_SUBSCRIBE_STATES["SUBSCRIBED"] = "SUBSCRIBED";
    REALTIME_SUBSCRIBE_STATES["TIMED_OUT"] = "TIMED_OUT";
    REALTIME_SUBSCRIBE_STATES["CLOSED"] = "CLOSED";
    REALTIME_SUBSCRIBE_STATES["CHANNEL_ERROR"] = "CHANNEL_ERROR";
})(REALTIME_SUBSCRIBE_STATES || (exports.REALTIME_SUBSCRIBE_STATES = REALTIME_SUBSCRIBE_STATES = {}));
exports.REALTIME_CHANNEL_STATES = constants_1.CHANNEL_STATES;
/** A channel is the basic building block of Realtime
 * and narrows the scope of data flow to subscribed clients.
 * You can think of a channel as a chatroom where participants are able to see who's online
 * and send and receive messages.
 */
class RealtimeChannel {
    get state() {
        return this.channelAdapter.state;
    }
    set state(state) {
        this.channelAdapter.state = state;
    }
    get joinedOnce() {
        return this.channelAdapter.joinedOnce;
    }
    get timeout() {
        return this.socket.timeout;
    }
    get joinPush() {
        return this.channelAdapter.joinPush;
    }
    get rejoinTimer() {
        return this.channelAdapter.rejoinTimer;
    }
    /**
     * Creates a channel that can broadcast messages, sync presence, and listen to Postgres changes.
     *
     * The topic determines which realtime stream you are subscribing to. Config options let you
     * enable acknowledgement for broadcasts, presence tracking, or private channels.
     *
     * @category Realtime
     *
     * @example Using supabase-js (recommended)
     * ```ts
     * import { createClient } from '@supabase/supabase-js'
     *
     * const supabase = createClient('https://xyzcompany.supabase.co', 'your-publishable-key')
     * const channel = supabase.channel('room1')
     * channel
     *   .on('broadcast', { event: 'cursor-pos' }, (payload) => console.log(payload))
     *   .subscribe()
     * ```
     *
     * @example Standalone import for bundle-sensitive environments
     * ```ts
     * import RealtimeClient from '@supabase/realtime-js'
     *
     * const client = new RealtimeClient('https://xyzcompany.supabase.co/realtime/v1', {
     *   params: { apikey: 'your-publishable-key' },
     * })
     * const channel = new RealtimeChannel('realtime:public:messages', { config: {} }, client)
     * ```
     */
    constructor(
    /** Topic name can be any string. */
    topic, params = { config: {} }, socket) {
        var _a, _b;
        this.topic = topic;
        this.params = params;
        this.socket = socket;
        this.bindings = {};
        this.subTopic = topic.replace(/^realtime:/i, '');
        this.params.config = Object.assign({
            broadcast: { ack: false, self: false },
            presence: { key: '', enabled: false },
            private: false,
        }, params.config);
        this.channelAdapter = new channelAdapter_1.default(this.socket.socketAdapter, topic, this.params);
        this.presence = new RealtimePresence_1.default(this);
        this._onClose(() => {
            this.socket._remove(this);
        });
        this._updateFilterTransform();
        this.broadcastEndpointURL = (0, transformers_1.httpEndpointURL)(this.socket.socketAdapter.endPointURL());
        this.private = this.params.config.private || false;
        if (!this.private && ((_b = (_a = this.params.config) === null || _a === void 0 ? void 0 : _a.broadcast) === null || _b === void 0 ? void 0 : _b.replay)) {
            throw new Error(`tried to use replay on public channel '${this.topic}'. It must be a private channel.`);
        }
    }
    /**
     * Subscribe registers your client with the server.
     *
     * The optional `callback` receives a `status` and, on failure, an `err` argument.
     * Log the full `err` so its `cause`, `name`, and any structured fields aren't hidden
     * behind `err.message`.
     *
     * @category Realtime
     *
     * @example Handling errors
     * ```js
     * supabase.channel('room1').subscribe((status, err) => {
     *   if (status === 'CHANNEL_ERROR' || status === 'TIMED_OUT') {
     *     // Log the full error: its `cause` often holds the underlying reason.
     *     console.error(status, err)
     *   }
     * })
     * ```
     */
    subscribe(callback, timeout = this.timeout) {
        var _a, _b, _c, _d;
        if (!this.socket.isConnected()) {
            this.socket.connect();
        }
        if (this.channelAdapter.isClosed()) {
            const { config: { broadcast, presence, private: isPrivate, postgres_changes_options }, } = this.params;
            const postgres_changes = (_b = (_a = this.bindings.postgres_changes) === null || _a === void 0 ? void 0 : _a.map((r) => r.filter)) !== null && _b !== void 0 ? _b : [];
            const presence_enabled = (!!this.bindings[REALTIME_LISTEN_TYPES.PRESENCE] &&
                this.bindings[REALTIME_LISTEN_TYPES.PRESENCE].length > 0) ||
                ((_c = this.params.config.presence) === null || _c === void 0 ? void 0 : _c.enabled) === true;
            const accessTokenPayload = {};
            const config = Object.assign({ broadcast, presence: Object.assign(Object.assign({}, presence), { enabled: presence_enabled }), postgres_changes, private: isPrivate }, (postgres_changes_options ? { postgres_changes_options } : {}));
            if (this.socket.accessTokenValue) {
                accessTokenPayload.access_token = this.socket.accessTokenValue;
            }
            this._onError((reason) => {
                callback === null || callback === void 0 ? void 0 : callback(REALTIME_SUBSCRIBE_STATES.CHANNEL_ERROR, (0, normalizeChannelError_1.normalizeChannelError)(reason));
            });
            this._onClose(() => callback === null || callback === void 0 ? void 0 : callback(REALTIME_SUBSCRIBE_STATES.CLOSED));
            this.updateJoinPayload(Object.assign({ config }, accessTokenPayload));
            this._updateFilterMessage();
            const joinTimeout = (postgres_changes_options === null || postgres_changes_options === void 0 ? void 0 : postgres_changes_options.wait) && postgres_changes.length > 0
                ? Math.max(timeout, ((_d = postgres_changes_options.timeout) !== null && _d !== void 0 ? _d : constants_1.DEFAULT_POSTGRES_CHANGES_WAIT_TIMEOUT) +
                    constants_1.POSTGRES_CHANGES_WAIT_ERROR_GRACE)
                : timeout;
            this.channelAdapter
                .subscribe(joinTimeout)
                .receive('ok', async ({ postgres_changes }) => {
                // Only refresh auth if using callback-based tokens
                if (!this.socket._isManualToken()) {
                    this.socket.setAuth();
                }
                if (postgres_changes === undefined) {
                    callback === null || callback === void 0 ? void 0 : callback(REALTIME_SUBSCRIBE_STATES.SUBSCRIBED);
                    return;
                }
                this._updatePostgresBindings(postgres_changes, callback);
            })
                .receive('error', (error) => {
                this.state = constants_1.CHANNEL_STATES.errored;
                const message = Object.values(error).join(', ') || 'error';
                callback === null || callback === void 0 ? void 0 : callback(REALTIME_SUBSCRIBE_STATES.CHANNEL_ERROR, new Error(message, { cause: error }));
            })
                .receive('timeout', () => {
                callback === null || callback === void 0 ? void 0 : callback(REALTIME_SUBSCRIBE_STATES.TIMED_OUT);
            });
        }
        return this;
    }
    _updatePostgresBindings(postgres_changes, callback) {
        var _a;
        const clientPostgresBindings = this.bindings.postgres_changes;
        const bindingsLen = (_a = clientPostgresBindings === null || clientPostgresBindings === void 0 ? void 0 : clientPostgresBindings.length) !== null && _a !== void 0 ? _a : 0;
        const newPostgresBindings = [];
        for (let i = 0; i < bindingsLen; i++) {
            const clientPostgresBinding = clientPostgresBindings[i];
            const { filter: { event, schema, table, filter }, } = clientPostgresBinding;
            const serverPostgresFilter = postgres_changes && postgres_changes[i];
            if (serverPostgresFilter &&
                serverPostgresFilter.event === event &&
                RealtimeChannel.isFilterValueEqual(serverPostgresFilter.schema, schema) &&
                RealtimeChannel.isFilterValueEqual(serverPostgresFilter.table, table) &&
                RealtimeChannel.isFilterValueEqual(serverPostgresFilter.filter, filter)) {
                newPostgresBindings.push(Object.assign(Object.assign({}, clientPostgresBinding), { id: serverPostgresFilter.id }));
            }
            else {
                this.unsubscribe();
                this.state = constants_1.CHANNEL_STATES.errored;
                callback === null || callback === void 0 ? void 0 : callback(REALTIME_SUBSCRIBE_STATES.CHANNEL_ERROR, new Error('mismatch between server and client bindings for postgres changes'));
                return;
            }
        }
        this.bindings.postgres_changes = newPostgresBindings;
        if (this.state != constants_1.CHANNEL_STATES.errored && callback) {
            callback(REALTIME_SUBSCRIBE_STATES.SUBSCRIBED);
        }
    }
    /**
     * Returns the current presence state for this channel.
     *
     * The shape is a map keyed by presence key (for example a user id) where each entry contains the
     * tracked metadata for that user.
     *
     * @category Realtime
     */
    presenceState() {
        return this.presence.state;
    }
    /**
     * Sends the supplied payload to the presence tracker so other subscribers can see that this
     * client is online. Use `untrack` to stop broadcasting presence for the same key.
     *
     * Tracking makes this client visible to other subscribers immediately, regardless of this
     * channel's `config.presence.enabled` setting or whether it has a `presence` listener — that
     * flag only affects whether *this* client receives presence updates from others (and, on
     * RLS-protected channels, whether it's authorized to do so).
     *
     * @category Realtime
     */
    async track(payload, opts = {}) {
        return await this.send({
            type: 'presence',
            event: 'track',
            payload,
        }, opts);
    }
    /**
     * Removes the current presence state for this client.
     *
     * @category Realtime
     */
    async untrack(opts = {}) {
        return await this.send({
            type: 'presence',
            event: 'untrack',
        }, opts);
    }
    /**
     * Listen to realtime events on this channel.
     * @category Realtime
     *
     * @remarks
     * - By default, Broadcast and Presence are enabled for all projects.
     * - By default, listening to database changes is disabled for new projects due to database performance and security concerns. You can turn it on by managing Realtime's [replication](/docs/guides/api#realtime-api-overview).
     * - You can receive the "previous" data for updates and deletes by setting the table's `REPLICA IDENTITY` to `FULL` (e.g., `ALTER TABLE your_table REPLICA IDENTITY FULL;`).
     * - Row level security is not applied to delete statements. When RLS is enabled and replica identity is set to full, only the primary key is sent to clients.
     *
     * @example Listen to broadcast messages
     * ```js
     * const channel = supabase.channel("room1")
     *
     * channel.on("broadcast", { event: "cursor-pos" }, (payload) => {
     *   console.log("Cursor position received!", payload);
     * }).subscribe((status) => {
     *   if (status === "SUBSCRIBED") {
     *     channel.send({
     *       type: "broadcast",
     *       event: "cursor-pos",
     *       payload: { x: Math.random(), y: Math.random() },
     *     });
     *   }
     * });
     * ```
     *
     * @example Listen to presence sync
     * ```js
     * const channel = supabase.channel('room1')
     * channel
     *   .on('presence', { event: 'sync' }, () => {
     *     console.log('Synced presence state: ', channel.presenceState())
     *   })
     *   .subscribe(async (status) => {
     *     if (status === 'SUBSCRIBED') {
     *       await channel.track({ online_at: new Date().toISOString() })
     *     }
     *   })
     * ```
     *
     * @example Listen to presence join
     * ```js
     * const channel = supabase.channel('room1')
     * channel
     *   .on('presence', { event: 'join' }, ({ newPresences }) => {
     *     console.log('Newly joined presences: ', newPresences)
     *   })
     *   .subscribe(async (status) => {
     *     if (status === 'SUBSCRIBED') {
     *       await channel.track({ online_at: new Date().toISOString() })
     *     }
     *   })
     * ```
     *
     * @example Listen to presence leave
     * ```js
     * const channel = supabase.channel('room1')
     * channel
     *   .on('presence', { event: 'leave' }, ({ leftPresences }) => {
     *     console.log('Newly left presences: ', leftPresences)
     *   })
     *   .subscribe(async (status) => {
     *     if (status === 'SUBSCRIBED') {
     *       await channel.track({ online_at: new Date().toISOString() })
     *       await channel.untrack()
     *     }
     *   })
     * ```
     *
     * Registering the same `postgres_changes` filter more than once on a channel is a no-op: the
     * duplicate is ignored and an error is logged, since the server only ever creates one
     * subscription per distinct filter.
     *
     * @example Listen to all database changes
     * ```js
     * supabase
     *   .channel('room1')
     *   .on('postgres_changes', { event: '*', schema: '*' }, payload => {
     *     console.log('Change received!', payload)
     *   })
     *   .subscribe()
     * ```
     *
     * @example Listen to a specific table
     * ```js
     * supabase
     *   .channel('room1')
     *   .on('postgres_changes', { event: '*', schema: 'public', table: 'countries' }, payload => {
     *     console.log('Change received!', payload)
     *   })
     *   .subscribe()
     * ```
     *
     * @example Listen to inserts
     * ```js
     * supabase
     *   .channel('room1')
     *   .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'countries' }, payload => {
     *     console.log('Change received!', payload)
     *   })
     *   .subscribe()
     * ```
     *
     * @exampleDescription Listen to updates
     * By default, Supabase will send only the updated record. If you want to receive the previous values as well you can
     * enable full replication for the table you are listening to:
     *
     * ```sql
     * alter table "your_table" replica identity full;
     * ```
     *
     * @example Listen to updates
     * ```js
     * supabase
     *   .channel('room1')
     *   .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'countries' }, payload => {
     *     console.log('Change received!', payload)
     *   })
     *   .subscribe()
     * ```
     *
     * @exampleDescription Listen to deletes
     * By default, Supabase does not send deleted records. If you want to receive the deleted record you can
     * enable full replication for the table you are listening to:
     *
     * ```sql
     * alter table "your_table" replica identity full;
     * ```
     *
     * @example Listen to deletes
     * ```js
     * supabase
     *   .channel('room1')
     *   .on('postgres_changes', { event: 'DELETE', schema: 'public', table: 'countries' }, payload => {
     *     console.log('Change received!', payload)
     *   })
     *   .subscribe()
     * ```
     *
     * @exampleDescription Listen to multiple events
     * You can chain listeners if you want to listen to multiple events for each table.
     *
     * @example Listen to multiple events
     * ```js
     * supabase
     *   .channel('room1')
     *   .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'countries' }, handleRecordInserted)
     *   .on('postgres_changes', { event: 'DELETE', schema: 'public', table: 'countries' }, handleRecordDeleted)
     *   .subscribe()
     * ```
     *
     * @exampleDescription Listen to row level changes
     * You can listen to individual rows using the format `{table}:{col}=eq.{val}` - where `{col}` is the column name, and `{val}` is the value which you want to match.
     *
     * @example Listen to row level changes
     * ```js
     * supabase
     *   .channel('room1')
     *   .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'countries', filter: 'id=eq.200' }, handleRecordUpdated)
     *   .subscribe()
     * ```
     */
    on(type, filter, callback) {
        const stateCheck = this.channelAdapter.isJoined() || this.channelAdapter.isJoining();
        const typeCheck = type === REALTIME_LISTEN_TYPES.PRESENCE || type === REALTIME_LISTEN_TYPES.POSTGRES_CHANGES;
        if (stateCheck && typeCheck) {
            this.socket.log('channel', `cannot add \`${type}\` callbacks for ${this.topic} after \`subscribe()\`.`);
            throw new Error(`cannot add \`${type}\` callbacks for ${this.topic} after \`subscribe()\`.`);
        }
        return this._on(type, filter, callback);
    }
    /**
     * Sends a broadcast message explicitly via REST API.
     *
     * This method always uses the REST API endpoint regardless of WebSocket connection state.
     * Useful when you want to guarantee REST delivery or when gradually migrating from implicit REST fallback.
     *
     * Payloads that are `ArrayBuffer` or `ArrayBufferView` (e.g. `Uint8Array`) are sent as
     * `application/octet-stream`; all other payloads are JSON-encoded.
     *
     * @param event The name of the broadcast event
     * @param payload Payload to be sent (required)
     * @param opts Options including timeout
     * @returns Promise resolving to object with success status, and error details if failed
     *
     * @category Realtime
     */
    async httpSend(event, payload, opts = {}) {
        var _a;
        if (payload === undefined || payload === null) {
            return Promise.reject(new Error('Payload is required for httpSend()'));
        }
        const isBinary = payload instanceof ArrayBuffer || ArrayBuffer.isView(payload);
        const headers = {
            apikey: this.socket.apiKey ? this.socket.apiKey : '',
            'Content-Type': isBinary ? 'application/octet-stream' : 'application/json',
        };
        if (this.socket.accessTokenValue) {
            headers['Authorization'] = `Bearer ${this.socket.accessTokenValue}`;
        }
        const url = new URL(this.broadcastEndpointURL);
        url.pathname += `/${encodeURIComponent(this.subTopic)}/events/${encodeURIComponent(event)}`;
        if (this.private) {
            url.searchParams.set('private', 'true');
        }
        const options = {
            method: 'POST',
            headers,
            body: isBinary ? payload : JSON.stringify(payload),
        };
        const response = await this._fetchWithTimeout(url.toString(), options, (_a = opts.timeout) !== null && _a !== void 0 ? _a : this.timeout);
        if (response.status === 202) {
            return { success: true };
        }
        if (response.status === 404) {
            return Promise.reject(new Error('httpSend() requires Realtime server v2.97.0 or newer; the endpoint returned 404. ' +
                'Update your Supabase CLI to a recent version, or upgrade the Realtime server in your self-hosted setup. ' +
                'See https://github.com/supabase/supabase-js/blob/master/packages/core/realtime-js/migrations/httpsend-server-version.md'));
        }
        let errorMessage = response.statusText;
        try {
            const errorBody = await response.json();
            errorMessage = errorBody.error || errorBody.message || errorMessage;
        }
        catch (_b) { }
        return Promise.reject(new Error(errorMessage));
    }
    /**
     * Sends a message into the channel.
     *
     * @param args Arguments to send to channel
     * @param args.type The type of event to send
     * @param args.event The name of the event being sent
     * @param args.payload Payload to be sent
     * @param opts Options to be used during the send process
     *
     * @category Realtime
     *
     * @remarks
     * - When using REST you don't need to subscribe to the channel
     * - REST calls are only available from 2.37.0 onwards
     * - If you create a channel only to send a REST broadcast, remove it from
     *   the client when the send completes
     *
     * @example Send a message via websocket
     * ```js
     * const channel = supabase.channel('room1')
     *
     * channel.subscribe((status) => {
     *   if (status === 'SUBSCRIBED') {
     *     channel.send({
     *       type: 'broadcast',
     *       event: 'cursor-pos',
     *       payload: { x: Math.random(), y: Math.random() },
     *     })
     *   }
     * })
     * ```
     *
     * @exampleResponse Send a message via websocket
     * ```js
     * ok | timed out | error
     * ```
     *
     * @example Send a message via REST
     * ```js
     * const channel = supabase.channel('room1')
     *
     * try {
     *   await channel.httpSend('cursor-pos', { x: Math.random(), y: Math.random() })
     * } finally {
     *   await supabase.removeChannel(channel)
     * }
     * ```
     */
    async send(args, opts = {}) {
        var _a, _b;
        if (!this.channelAdapter.canPush() && args.type === 'broadcast') {
            const fallbackWarning = 'Realtime send() is automatically falling back to REST API. ' +
                'This behavior will be deprecated in the future. ' +
                'Please use httpSend() explicitly for REST delivery.';
            if (this.socket.hasLogger()) {
                this.socket.log('channel', fallbackWarning);
            }
            else {
                console.warn(fallbackWarning);
            }
            const { event, payload: endpoint_payload } = args;
            const headers = {
                apikey: this.socket.apiKey ? this.socket.apiKey : '',
                'Content-Type': 'application/json',
            };
            if (this.socket.accessTokenValue) {
                headers['Authorization'] = `Bearer ${this.socket.accessTokenValue}`;
            }
            const options = {
                method: 'POST',
                headers,
                body: JSON.stringify({
                    messages: [
                        {
                            topic: this.subTopic,
                            event,
                            payload: endpoint_payload,
                            private: this.private,
                        },
                    ],
                }),
            };
            try {
                const response = await this._fetchWithTimeout(this.broadcastEndpointURL, options, (_a = opts.timeout) !== null && _a !== void 0 ? _a : this.timeout);
                await ((_b = response.body) === null || _b === void 0 ? void 0 : _b.cancel());
                return response.ok ? 'ok' : 'error';
            }
            catch (error) {
                if (error instanceof Error && error.name === 'AbortError') {
                    return 'timed out';
                }
                else {
                    return 'error';
                }
            }
        }
        else {
            return new Promise((resolve) => {
                var _a, _b, _c;
                const push = this.channelAdapter.push(args.type, args, opts.timeout || this.timeout);
                if (args.type === 'broadcast' && !((_c = (_b = (_a = this.params) === null || _a === void 0 ? void 0 : _a.config) === null || _b === void 0 ? void 0 : _b.broadcast) === null || _c === void 0 ? void 0 : _c.ack)) {
                    resolve('ok');
                }
                push.receive('ok', () => resolve('ok'));
                push.receive('error', () => resolve('error'));
                push.receive('timeout', () => resolve('timed out'));
            });
        }
    }
    /**
     * Updates the payload that will be sent the next time the channel joins (reconnects).
     * Useful for rotating access tokens or updating config without re-creating the channel.
     *
     * @category Realtime
     */
    updateJoinPayload(payload) {
        this.channelAdapter.updateJoinPayload(payload);
    }
    /**
     * Leaves the channel.
     *
     * Unsubscribes from server events, and instructs channel to terminate on server.
     * Triggers onClose() hooks.
     *
     * To receive leave acknowledgements, use the a `receive` hook to bind to the server ack, ie:
     * channel.unsubscribe().receive("ok", () => alert("left!") )
     *
     * @category Realtime
     */
    async unsubscribe(timeout = this.timeout) {
        return new Promise((resolve) => {
            this.channelAdapter
                .unsubscribe(timeout)
                .receive('ok', () => resolve('ok'))
                .receive('timeout', () => resolve('timed out'))
                .receive('error', () => resolve('error'));
        });
    }
    /**
     * Destroys and stops related timers.
     *
     * @category Realtime
     */
    teardown() {
        this.channelAdapter.teardown();
    }
    /** @internal */
    async _fetchWithTimeout(url, options, timeout) {
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), timeout);
        const response = await this.socket.fetch(url, Object.assign(Object.assign({}, options), { signal: controller.signal }));
        clearTimeout(id);
        return response;
    }
    /** @internal */
    _on(type, filter, callback) {
        var _a;
        const typeLower = type.toLocaleLowerCase();
        // Serialize a postgres_changes filter builder into its string form so the
        // rest of the pipeline (join payload, server binding match) sees a string.
        // Duck-type `build()` in addition to `instanceof` so a builder constructed
        // against a duplicate copy of the package (separate module realm) still works.
        const filterValue = filter === null || filter === void 0 ? void 0 : filter.filter;
        if (filterValue instanceof RealtimePostgresFilterBuilder_1.RealtimePostgresFilterBuilder ||
            (typeof filterValue === 'object' &&
                filterValue !== null &&
                typeof filterValue.build === 'function')) {
            filter = Object.assign(Object.assign({}, filter), { filter: filterValue.build() });
        }
        // The server collapses identical postgres_changes filters, so keeping a duplicate here would
        // desync the client and server binding lists and make `subscribe()` fail with a mismatch.
        if (typeLower === REALTIME_LISTEN_TYPES.POSTGRES_CHANGES) {
            const duplicate = (_a = this.bindings[typeLower]) === null || _a === void 0 ? void 0 : _a.find((bind) => RealtimeChannel.isSamePostgresFilter(bind.filter, filter));
            if (duplicate) {
                this.socket.log('error', `duplicate \`postgres_changes\` binding for ${this.topic} ignored`, filter);
                return this;
            }
        }
        const ref = this.channelAdapter.on(type, callback);
        const binding = {
            type: typeLower,
            filter: filter,
            callback: callback,
            ref: ref,
        };
        if (this.bindings[typeLower]) {
            this.bindings[typeLower].push(binding);
        }
        else {
            this.bindings[typeLower] = [binding];
        }
        this._updateFilterMessage();
        return this;
    }
    /**
     * Registers a callback that will be executed when the channel closes.
     *
     * @internal
     */
    _onClose(callback) {
        this.channelAdapter.onClose(callback);
    }
    /**
     * Registers a callback that will be executed when the channel encounteres an error.
     *
     * @internal
     */
    _onError(callback) {
        this.channelAdapter.onError(callback);
    }
    /** @internal */
    _updateFilterMessage() {
        this.channelAdapter.updateFilterBindings((binding, payload, ref) => {
            var _a, _b, _c, _d, _e, _f, _g;
            const typeLower = binding.event.toLocaleLowerCase();
            if (this._notThisChannelEvent(typeLower, ref)) {
                return false;
            }
            const bind = (_a = this.bindings[typeLower]) === null || _a === void 0 ? void 0 : _a.find((bind) => bind.ref === binding.ref);
            if (!bind) {
                return true;
            }
            if (['broadcast', 'presence', 'postgres_changes'].includes(typeLower)) {
                if ('id' in bind) {
                    const bindId = bind.id;
                    const bindEvent = (_b = bind.filter) === null || _b === void 0 ? void 0 : _b.event;
                    return (bindId &&
                        ((_c = payload.ids) === null || _c === void 0 ? void 0 : _c.includes(bindId)) &&
                        (bindEvent === '*' ||
                            (bindEvent === null || bindEvent === void 0 ? void 0 : bindEvent.toLocaleLowerCase()) === ((_d = payload.data) === null || _d === void 0 ? void 0 : _d.type.toLocaleLowerCase())));
                }
                else {
                    const bindEvent = (_f = (_e = bind === null || bind === void 0 ? void 0 : bind.filter) === null || _e === void 0 ? void 0 : _e.event) === null || _f === void 0 ? void 0 : _f.toLocaleLowerCase();
                    return bindEvent === '*' || bindEvent === ((_g = payload === null || payload === void 0 ? void 0 : payload.event) === null || _g === void 0 ? void 0 : _g.toLocaleLowerCase());
                }
            }
            else {
                return bind.type.toLocaleLowerCase() === typeLower;
            }
        });
    }
    /** @internal */
    _notThisChannelEvent(event, ref) {
        const { close, error, leave, join } = constants_1.CHANNEL_EVENTS;
        const events = [close, error, leave, join];
        return ref && events.includes(event) && ref !== this.joinPush.ref;
    }
    /** @internal */
    _updateFilterTransform() {
        this.channelAdapter.updatePayloadTransform((event, payload, ref) => {
            if (typeof payload === 'object' && 'ids' in payload) {
                const postgresChanges = payload.data;
                const { schema, table, commit_timestamp, type, errors } = postgresChanges;
                const enrichedPayload = {
                    schema: schema,
                    table: table,
                    commit_timestamp: commit_timestamp,
                    eventType: type,
                    new: {},
                    old: {},
                    errors: errors,
                };
                return Object.assign(Object.assign({}, enrichedPayload), this._getPayloadRecords(postgresChanges));
            }
            return payload;
        });
    }
    copyBindings(other) {
        if (this.joinedOnce) {
            throw new Error('cannot copy bindings into joined channel');
        }
        for (const kind in other.bindings) {
            for (const binding of other.bindings[kind]) {
                this._on(binding.type, binding.filter, binding.callback);
            }
        }
    }
    /**
     * Compares two optional filter values for equality.
     * Treats undefined, null, and empty string as equivalent empty values.
     * @internal
     */
    static isFilterValueEqual(serverValue, clientValue) {
        const normalizedServer = serverValue !== null && serverValue !== void 0 ? serverValue : undefined;
        const normalizedClient = clientValue !== null && clientValue !== void 0 ? clientValue : undefined;
        return normalizedServer === normalizedClient;
    }
    /**
     * Two `postgres_changes` filters are the same when the server would collapse them into a single
     * subscription.
     * @internal
     */
    static isSamePostgresFilter(a, b) {
        var _a, _b, _c, _d;
        const selectA = (_b = (_a = a === null || a === void 0 ? void 0 : a.select) === null || _a === void 0 ? void 0 : _a.join()) !== null && _b !== void 0 ? _b : undefined;
        const selectB = (_d = (_c = b === null || b === void 0 ? void 0 : b.select) === null || _c === void 0 ? void 0 : _c.join()) !== null && _d !== void 0 ? _d : undefined;
        return ((a === null || a === void 0 ? void 0 : a.event) === (b === null || b === void 0 ? void 0 : b.event) &&
            RealtimeChannel.isFilterValueEqual(a === null || a === void 0 ? void 0 : a.schema, b === null || b === void 0 ? void 0 : b.schema) &&
            RealtimeChannel.isFilterValueEqual(a === null || a === void 0 ? void 0 : a.table, b === null || b === void 0 ? void 0 : b.table) &&
            RealtimeChannel.isFilterValueEqual(a === null || a === void 0 ? void 0 : a.filter, b === null || b === void 0 ? void 0 : b.filter) &&
            selectA === selectB);
    }
    /** @internal */
    _getPayloadRecords(payload) {
        const records = {
            new: {},
            old: {},
        };
        if (payload.type === 'INSERT' || payload.type === 'UPDATE') {
            records.new = Transformers.convertChangeData(payload.columns, payload.record);
        }
        if (payload.type === 'UPDATE' || payload.type === 'DELETE') {
            records.old = Transformers.convertChangeData(payload.columns, payload.old_record);
        }
        return records;
    }
}
exports.default = RealtimeChannel;
//# sourceMappingURL=RealtimeChannel.js.map