import WebSocketFactory from './lib/websocket-factory';
import { CHANNEL_EVENTS, CONNECTION_STATE, DEFAULT_VERSION, DEFAULT_TIMEOUT, DEFAULT_VSN, VSN_1_0_0, VSN_2_0_0, } from './lib/constants';
import Serializer from './lib/serializer';
import { httpEndpointURL } from './lib/transformers';
import RealtimeChannel from './RealtimeChannel';
import SocketAdapter from './phoenix/socketAdapter';
// Connection-related constants
const CONNECTION_TIMEOUTS = {
    HEARTBEAT_INTERVAL: 25000,
    RECONNECT_DELAY: 10,
    HEARTBEAT_TIMEOUT_FALLBACK: 100,
};
const RECONNECT_INTERVALS = [1000, 2000, 5000, 10000];
const DEFAULT_RECONNECT_FALLBACK = 10000;
function createMemorySessionStorage() {
    const store = new Map();
    return {
        get length() {
            return store.size;
        },
        clear() {
            store.clear();
        },
        getItem(key) {
            return store.has(key) ? store.get(key) : null;
        },
        key(index) {
            var _a;
            return (_a = Array.from(store.keys())[index]) !== null && _a !== void 0 ? _a : null;
        },
        removeItem(key) {
            store.delete(key);
        },
        setItem(key, value) {
            store.set(key, String(value));
        },
    };
}
function resolveSessionStorage() {
    try {
        if (typeof globalThis !== 'undefined' && globalThis.sessionStorage) {
            return globalThis.sessionStorage;
        }
    }
    catch (_a) {
        // Property access on `sessionStorage` itself throws in restricted-storage browsers.
    }
    return createMemorySessionStorage();
}
const WORKER_SCRIPT = `
  addEventListener("message", (e) => {
    if (e.data.event === "start") {
      setInterval(() => postMessage({ event: "keepAlive" }), e.data.interval);
    }
  });`;
export default class RealtimeClient {
    get endPoint() {
        return this.socketAdapter.endPoint;
    }
    get timeout() {
        return this.socketAdapter.timeout;
    }
    get transport() {
        return this.socketAdapter.transport;
    }
    get heartbeatCallback() {
        return this.socketAdapter.heartbeatCallback;
    }
    get heartbeatIntervalMs() {
        return this.socketAdapter.heartbeatIntervalMs;
    }
    get heartbeatTimer() {
        if (this.worker) {
            return this._workerHeartbeatTimer;
        }
        return this.socketAdapter.heartbeatTimer;
    }
    get pendingHeartbeatRef() {
        if (this.worker) {
            return this._pendingWorkerHeartbeatRef;
        }
        return this.socketAdapter.pendingHeartbeatRef;
    }
    get reconnectTimer() {
        return this.socketAdapter.reconnectTimer;
    }
    get vsn() {
        return this.socketAdapter.vsn;
    }
    get encode() {
        return this.socketAdapter.encode;
    }
    get decode() {
        return this.socketAdapter.decode;
    }
    get reconnectAfterMs() {
        return this.socketAdapter.reconnectAfterMs;
    }
    get sendBuffer() {
        return this.socketAdapter.sendBuffer;
    }
    get stateChangeCallbacks() {
        return this.socketAdapter.stateChangeCallbacks;
    }
    /**
     * Initializes the Socket.
     *
     * @param endPoint The string WebSocket endpoint, ie, "ws://example.com/socket", "wss://example.com", "/socket" (inherited host & protocol)
     * @param options.transport The Websocket Transport, for example WebSocket. This can be a custom implementation
     * @param options.timeout The default timeout in milliseconds to trigger push timeouts.
     * @param options.params The optional params to pass when connecting.
     * @param options.headers Deprecated: headers cannot be set on websocket connections and this option will be removed in the future.
     * @param options.heartbeatIntervalMs The millisec interval to send a heartbeat message.
     * @param options.heartbeatCallback The optional function to handle heartbeat status and latency.
     * @param options.logger The optional function for specialized logging, ie: logger: (kind, msg, data) => { console.log(`${kind}: ${msg}`, data) }
     * @param options.logLevel Sets the log level for Realtime
     * @param options.encode The function to encode outgoing messages. Defaults to JSON: (payload, callback) => callback(JSON.stringify(payload))
     * @param options.decode The function to decode incoming messages. Defaults to Serializer's decode.
     * @param options.reconnectAfterMs he optional function that returns the millsec reconnect interval. Defaults to stepped backoff off.
     * @param options.worker Use Web Worker to set a side flow. Defaults to false.
     * @param options.workerUrl The URL of the worker script. Defaults to https://realtime.supabase.com/worker.js that includes a heartbeat event call to keep the connection alive.
     * @param options.vsn The protocol version to use when connecting. Supported versions are "1.0.0" and "2.0.0". Defaults to "2.0.0".
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
     * client.connect()
     * ```
     */
    constructor(endPoint, options) {
        var _a;
        this.channels = new Array();
        this.accessTokenValue = null;
        this.accessToken = null;
        this.apiKey = null;
        this.httpEndpoint = '';
        /** @deprecated headers cannot be set on websocket connections */
        this.headers = {};
        this.params = {};
        this.ref = 0;
        this.serializer = new Serializer();
        this._manuallySetToken = false;
        this._authPromise = null;
        this._authGeneration = 0;
        this._workerHeartbeatTimer = undefined;
        this._pendingWorkerHeartbeatRef = null;
        this._pendingDisconnectTimer = null;
        this._disconnectOnEmptyChannelsAfterMs = 0;
        /**
         * Use either custom fetch, if provided, or default fetch to make HTTP requests
         *
         * @internal
         */
        this._resolveFetch = (customFetch) => {
            if (customFetch) {
                return (...args) => customFetch(...args);
            }
            return (...args) => fetch(...args);
        };
        // Validate required parameters
        if (!((_a = options === null || options === void 0 ? void 0 : options.params) === null || _a === void 0 ? void 0 : _a.apikey)) {
            throw new Error('API key is required to connect to Realtime');
        }
        this.apiKey = options.params.apikey;
        const socketAdapterOptions = this._initializeOptions(options);
        this.socketAdapter = new SocketAdapter(endPoint, socketAdapterOptions);
        this.httpEndpoint = httpEndpointURL(endPoint);
        this.fetch = this._resolveFetch(options === null || options === void 0 ? void 0 : options.fetch);
    }
    /**
     * Connects the socket, unless already connected.
     *
     * @category Realtime
     */
    connect() {
        // Skip if already connecting, disconnecting, or connected
        if (this.isConnecting() || this.isDisconnecting() || this.isConnected()) {
            return;
        }
        // Trigger auth if needed and not already in progress
        // This ensures auth is called for standalone RealtimeClient usage
        // while avoiding race conditions with SupabaseClient's immediate setAuth call
        if (this.accessToken && !this._authPromise) {
            this._setAuthSafely('connect');
        }
        this._setupConnectionHandlers();
        try {
            this.socketAdapter.connect();
        }
        catch (error) {
            const errorMessage = error.message;
            throw new Error(`WebSocket not available: ${errorMessage}`);
        }
        this._handleNodeJsRaceCondition();
    }
    /**
     * Returns the URL of the websocket.
     * @returns string The URL of the websocket.
     *
     * @category Realtime
     */
    endpointURL() {
        return this.socketAdapter.endPointURL();
    }
    /**
     * Disconnects the socket.
     *
     * @param code A numeric status code to send on disconnect.
     * @param reason A custom reason for the disconnect.
     *
     * @category Realtime
     */
    async disconnect(code, reason) {
        this._cancelPendingDisconnect();
        if (this.isDisconnecting()) {
            return 'ok';
        }
        return await this.socketAdapter.disconnect(() => {
            clearInterval(this._workerHeartbeatTimer);
            this._terminateWorker();
        }, code, reason);
    }
    /**
     * Returns all created channels
     *
     * @category Realtime
     */
    getChannels() {
        return this.channels;
    }
    /**
     * Unsubscribes, removes and tears down a single channel
     * @param channel A RealtimeChannel instance
     *
     * @category Realtime
     */
    async removeChannel(channel) {
        const status = await channel.unsubscribe();
        if (status === 'ok') {
            channel.teardown();
        }
        return status;
    }
    /**
     * Unsubscribes, removes and tears down all channels
     *
     * @category Realtime
     */
    async removeAllChannels() {
        const promises = this.channels.map(async (channel) => {
            const result = await channel.unsubscribe();
            channel.teardown();
            return result;
        });
        const result = await Promise.all(promises);
        await this.disconnect();
        return result;
    }
    /**
     * Logs the message.
     *
     * For customized logging, `this.logger` can be overridden in Client constructor.
     *
     * @category Realtime
     */
    log(kind, msg, data) {
        this.socketAdapter.log(kind, msg, data);
    }
    /**
     * Returns true if a custom `logger` has been configured on this client.
     *
     * @category Realtime
     */
    hasLogger() {
        return this.socketAdapter.hasLogger();
    }
    /**
     * Returns the current state of the socket.
     *
     * @category Realtime
     */
    connectionState() {
        return this.socketAdapter.connectionState() || CONNECTION_STATE.closed;
    }
    /**
     * Returns `true` is the connection is open.
     *
     * @category Realtime
     */
    isConnected() {
        return this.socketAdapter.isConnected();
    }
    /**
     * Returns `true` if the connection is currently connecting.
     *
     * @category Realtime
     */
    isConnecting() {
        return this.socketAdapter.isConnecting();
    }
    /**
     * Returns `true` if the connection is currently disconnecting.
     *
     * @category Realtime
     */
    isDisconnecting() {
        return this.socketAdapter.isDisconnecting();
    }
    /**
     * Creates (or reuses) a {@link RealtimeChannel} for the provided topic.
     *
     * Topics are automatically prefixed with `realtime:` to match the Realtime service.
     * If a channel with the same topic already exists it will be returned instead of creating
     * a duplicate connection.
     *
     * @category Realtime
     */
    channel(topic, params = { config: {} }) {
        const realtimeTopic = `realtime:${topic}`;
        const exists = this.getChannels().find((c) => c.topic === realtimeTopic);
        if (!exists) {
            const chan = new RealtimeChannel(`realtime:${topic}`, params, this);
            this._cancelPendingDisconnect();
            this.channels.push(chan);
            return chan;
        }
        else {
            return exists;
        }
    }
    /**
     * Push out a message if the socket is connected.
     *
     * If the socket is not connected, the message gets enqueued within a local buffer, and sent out when a connection is next established.
     *
     * @category Realtime
     */
    push(data) {
        this.socketAdapter.push(data);
    }
    /**
     * Sets the JWT access token used for channel subscription authorization and Realtime RLS.
     *
     * If param is null it will use the `accessToken` callback function or the token set on the client.
     *
     * On callback used, it will set the value of the token internal to the client.
     *
     * When a token is explicitly provided AND no `accessToken` callback is configured,
     * it will be preserved across channel operations (including removeChannel and
     * resubscribe) and the client stays in manual-token mode.
     *
     * When an `accessToken` callback IS configured, the callback is the source of truth:
     * the client remains in callback mode and continues to refresh from it on heartbeat,
     * even after a bootstrap/override `setAuth(token)` call.
     *
     * @param token A JWT string to override the token set on the client.
     *
     * @example Setting the authorization header
     * // Use a manual token (preserved across resubscribes when no accessToken callback is set)
     * client.realtime.setAuth('my-custom-jwt')
     *
     * // Switch back to using the accessToken callback
     * client.realtime.setAuth()
     *
     * @category Realtime
     */
    async setAuth(token = null) {
        const authGeneration = ++this._authGeneration;
        const authPromise = this._performAuth(token, authGeneration);
        if (authGeneration === this._authGeneration) {
            this._authPromise = authPromise;
        }
        try {
            await authPromise;
        }
        finally {
            if (this._authPromise === authPromise) {
                this._authPromise = null;
            }
        }
    }
    /**
     * Returns true if the current access token was explicitly set via setAuth(token),
     * false if it was obtained via the accessToken callback.
     * @internal
     */
    _isManualToken() {
        return this._manuallySetToken;
    }
    /**
     * Sends a heartbeat message if the socket is connected.
     *
     * @category Realtime
     */
    async sendHeartbeat() {
        this.socketAdapter.sendHeartbeat();
    }
    /**
     * Sets a callback that receives lifecycle events for internal heartbeat messages.
     * Useful for instrumenting connection health (e.g. sent/ok/timeout).
     *
     * @category Realtime
     */
    onHeartbeat(callback) {
        this.socketAdapter.heartbeatCallback = this._wrapHeartbeatCallback(callback);
    }
    /**
     * Return the next message ref, accounting for overflows
     *
     * @internal
     */
    _makeRef() {
        return this.socketAdapter.makeRef();
    }
    /**
     * Removes a channel from RealtimeClient
     *
     * @param channel An open subscription.
     *
     * @internal
     */
    _remove(channel) {
        this.channels = this.channels.filter((c) => c.topic !== channel.topic);
        if (this.channels.length === 0) {
            this.log('transport', 'no channels remaining, scheduling disconnect');
            this._schedulePendingDisconnect();
        }
    }
    /** @internal */
    _schedulePendingDisconnect() {
        this._cancelPendingDisconnect();
        if (this._disconnectOnEmptyChannelsAfterMs === 0) {
            this.log('transport', 'disconnecting immediately - no channels');
            this.disconnect();
            return;
        }
        this._pendingDisconnectTimer = setTimeout(() => {
            this._pendingDisconnectTimer = null;
            if (this.channels.length === 0) {
                this.log('transport', 'deferred disconnect fired - no channels, disconnecting');
                this.disconnect();
            }
        }, this._disconnectOnEmptyChannelsAfterMs);
        this.log('transport', `deferred disconnect scheduled in ${this._disconnectOnEmptyChannelsAfterMs}ms`);
    }
    /** @internal */
    _cancelPendingDisconnect() {
        if (this._pendingDisconnectTimer !== null) {
            this.log('transport', 'pending disconnect cancelled - channel activity detected');
            clearTimeout(this._pendingDisconnectTimer);
            this._pendingDisconnectTimer = null;
        }
    }
    /**
     * Perform the actual auth operation
     * @internal
     */
    async _performAuth(token, authGeneration) {
        let tokenToSend;
        let isManualToken = false;
        if (token) {
            tokenToSend = token;
            // Track if this is a manually-provided token
            isManualToken = true;
        }
        else if (this.accessToken) {
            // Call the accessToken callback to get fresh token
            try {
                tokenToSend = await this.accessToken();
            }
            catch (e) {
                this.log('error', 'Error fetching access token from callback', e);
                // Fall back to cached value if callback fails
                tokenToSend = this.accessTokenValue;
            }
        }
        else {
            tokenToSend = this.accessTokenValue;
        }
        if (authGeneration !== this._authGeneration) {
            return;
        }
        // Track whether this token was manually set or fetched via callback.
        // The callback is the source of truth for token refresh
        if (this.accessToken) {
            this._manuallySetToken = false;
        }
        else if (isManualToken) {
            this._manuallySetToken = true;
        }
        if (this.accessTokenValue != tokenToSend) {
            this.accessTokenValue = tokenToSend;
            this.channels.forEach((channel) => {
                const payload = {
                    access_token: tokenToSend,
                    version: DEFAULT_VERSION,
                };
                channel.updateJoinPayload(payload);
                if (channel.joinedOnce && channel.channelAdapter.isJoined()) {
                    channel.channelAdapter.push(CHANNEL_EVENTS.access_token, {
                        access_token: tokenToSend,
                    });
                }
            });
        }
    }
    /**
     * Wait for any in-flight auth operations to complete
     * @internal
     */
    async _waitForAuthIfNeeded() {
        if (this._authPromise) {
            await this._authPromise;
        }
    }
    /**
     * Safely call setAuth with standardized error handling
     * @internal
     */
    _setAuthSafely(context = 'general') {
        // Only refresh auth if using callback-based tokens
        if (!this._isManualToken()) {
            this.setAuth().catch((e) => {
                this.log('error', `Error setting auth in ${context}`, e);
            });
        }
    }
    /** @internal */
    _setupConnectionHandlers() {
        this.socketAdapter.onOpen(() => {
            const authPromise = this._authPromise ||
                (this.accessToken && !this.accessTokenValue ? this.setAuth() : Promise.resolve());
            authPromise.catch((e) => {
                this.log('error', 'error waiting for auth on connect', e);
            });
            if (this.worker && !this.workerRef) {
                this._startWorkerHeartbeat();
            }
        });
        this.socketAdapter.onClose(() => {
            if (this.worker && this.workerRef) {
                this._terminateWorker();
            }
        });
        this.socketAdapter.onMessage((message) => {
            if (message.ref && message.ref === this._pendingWorkerHeartbeatRef) {
                this._pendingWorkerHeartbeatRef = null;
            }
        });
    }
    /** @internal */
    _handleNodeJsRaceCondition() {
        if (this.socketAdapter.isConnected()) {
            // hack: ensure onConnOpen is called
            this.socketAdapter.getSocket().onConnOpen();
        }
    }
    /** @internal */
    _wrapHeartbeatCallback(heartbeatCallback) {
        return (status, latency) => {
            if (status === 'disconnected')
                return;
            if (status == 'sent')
                this._setAuthSafely();
            if (heartbeatCallback)
                heartbeatCallback(status, latency);
        };
    }
    /** @internal */
    _startWorkerHeartbeat() {
        if (this.workerUrl) {
            this.log('worker', `starting worker for from ${this.workerUrl}`);
        }
        else {
            this.log('worker', `starting default worker`);
        }
        const objectUrl = this._workerObjectUrl(this.workerUrl);
        this.workerRef = new Worker(objectUrl);
        this.workerRef.onerror = (error) => {
            this.log('worker', 'worker error', error.message);
            this._terminateWorker();
            this.disconnect();
        };
        this.workerRef.onmessage = (event) => {
            if (event.data.event === 'keepAlive') {
                this.sendHeartbeat();
            }
        };
        this.workerRef.postMessage({
            event: 'start',
            interval: this.heartbeatIntervalMs,
        });
    }
    /**
     * Terminate the Web Worker and clear the reference
     * @internal
     */
    _terminateWorker() {
        if (this.workerRef) {
            this.log('worker', 'terminating worker');
            this.workerRef.terminate();
            this.workerRef = undefined;
        }
    }
    /** @internal */
    _workerObjectUrl(url) {
        let result_url;
        if (url) {
            result_url = url;
        }
        else {
            const blob = new Blob([WORKER_SCRIPT], { type: 'application/javascript' });
            result_url = URL.createObjectURL(blob);
        }
        return result_url;
    }
    /**
     * Initialize socket options with defaults
     * @internal
     */
    _initializeOptions(options) {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l, _m;
        this.worker = (_a = options === null || options === void 0 ? void 0 : options.worker) !== null && _a !== void 0 ? _a : false;
        this.accessToken = (_b = options === null || options === void 0 ? void 0 : options.accessToken) !== null && _b !== void 0 ? _b : null;
        const result = {};
        result.timeout = (_c = options === null || options === void 0 ? void 0 : options.timeout) !== null && _c !== void 0 ? _c : DEFAULT_TIMEOUT;
        result.heartbeatIntervalMs =
            (_d = options === null || options === void 0 ? void 0 : options.heartbeatIntervalMs) !== null && _d !== void 0 ? _d : CONNECTION_TIMEOUTS.HEARTBEAT_INTERVAL;
        this._disconnectOnEmptyChannelsAfterMs =
            (_e = options === null || options === void 0 ? void 0 : options.disconnectOnEmptyChannelsAfterMs) !== null && _e !== void 0 ? _e : 2 * ((_f = options === null || options === void 0 ? void 0 : options.heartbeatIntervalMs) !== null && _f !== void 0 ? _f : CONNECTION_TIMEOUTS.HEARTBEAT_INTERVAL);
        // @ts-ignore - mismatch between phoenix and supabase
        result.transport = (_g = options === null || options === void 0 ? void 0 : options.transport) !== null && _g !== void 0 ? _g : WebSocketFactory.getWebSocketConstructor();
        result.params = options === null || options === void 0 ? void 0 : options.params;
        result.logger = options === null || options === void 0 ? void 0 : options.logger;
        result.heartbeatCallback = this._wrapHeartbeatCallback(options === null || options === void 0 ? void 0 : options.heartbeatCallback);
        result.sessionStorage = (_h = options === null || options === void 0 ? void 0 : options.sessionStorage) !== null && _h !== void 0 ? _h : resolveSessionStorage();
        result.reconnectAfterMs =
            (_j = options === null || options === void 0 ? void 0 : options.reconnectAfterMs) !== null && _j !== void 0 ? _j : ((tries) => {
                return RECONNECT_INTERVALS[tries - 1] || DEFAULT_RECONNECT_FALLBACK;
            });
        let defaultEncode;
        let defaultDecode;
        const vsn = (_k = options === null || options === void 0 ? void 0 : options.vsn) !== null && _k !== void 0 ? _k : DEFAULT_VSN;
        switch (vsn) {
            case VSN_1_0_0:
                defaultEncode = (payload, callback) => {
                    return callback(JSON.stringify(payload));
                };
                defaultDecode = (payload, callback) => {
                    return callback(JSON.parse(payload));
                };
                break;
            case VSN_2_0_0:
                defaultEncode = this.serializer.encode.bind(this.serializer);
                defaultDecode = this.serializer.decode.bind(this.serializer);
                break;
            default:
                throw new Error(`Unsupported serializer version: ${result.vsn}`);
        }
        result.vsn = vsn;
        result.encode = (_l = options === null || options === void 0 ? void 0 : options.encode) !== null && _l !== void 0 ? _l : defaultEncode;
        result.decode = (_m = options === null || options === void 0 ? void 0 : options.decode) !== null && _m !== void 0 ? _m : defaultDecode;
        result.beforeReconnect = this._reconnectAuth.bind(this);
        if ((options === null || options === void 0 ? void 0 : options.logLevel) || (options === null || options === void 0 ? void 0 : options.log_level)) {
            this.logLevel = options.logLevel || options.log_level;
            result.params = Object.assign(Object.assign({}, result.params), { log_level: this.logLevel });
        }
        // Handle worker setup
        if (this.worker) {
            if (typeof window !== 'undefined' && !window.Worker) {
                throw new Error('Web Worker is not supported');
            }
            this.workerUrl = options === null || options === void 0 ? void 0 : options.workerUrl;
            result.autoSendHeartbeat = !this.worker;
        }
        return result;
    }
    /** @internal */
    async _reconnectAuth() {
        await this._waitForAuthIfNeeded();
        if (!this.isConnected()) {
            this.connect();
        }
    }
}
//# sourceMappingURL=RealtimeClient.js.map