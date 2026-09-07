import { WebSocketLike } from './lib/websocket-factory';
import Serializer from './lib/serializer';
import RealtimeChannel from './RealtimeChannel';
import type { RealtimeChannelOptions } from './RealtimeChannel';
import type { HeartbeatCallback, Encode, Decode, Timer, Vsn } from './phoenix/types';
type Fetch = typeof fetch;
export type LogLevel = 'info' | 'warn' | 'error' | (string & {});
export type RealtimeMessage = {
    topic: string;
    event: string;
    payload: any;
    ref: string;
    join_ref?: string;
};
export type RealtimeRemoveChannelResponse = 'ok' | 'timed out' | 'error' | (string & {});
export type HeartbeatStatus = 'sent' | 'ok' | 'error' | 'timeout' | 'disconnected' | (string & {});
export type HeartbeatTimer = ReturnType<typeof setTimeout> | undefined;
/**
 * Minimal WebSocket constructor interface that RealtimeClient can work with.
 * Supply a compatible implementation (native WebSocket, `ws`, etc) when running outside the browser.
 */
export interface WebSocketLikeConstructor {
    new (address: string | URL, subprotocols?: string | string[] | undefined): WebSocketLike;
    [key: string]: any;
}
export type RealtimeClientOptions = {
    transport?: WebSocketLikeConstructor;
    timeout?: number;
    heartbeatIntervalMs?: number;
    heartbeatCallback?: (status: HeartbeatStatus, latency?: number) => void;
    vsn?: string;
    logger?: (kind: string, msg: string, data?: any) => void;
    encode?: Encode<void>;
    decode?: Decode<void>;
    reconnectAfterMs?: (tries: number) => number;
    headers?: {
        [key: string]: string;
    };
    params?: {
        [key: string]: any;
    };
    log_level?: LogLevel;
    logLevel?: LogLevel;
    fetch?: Fetch;
    worker?: boolean;
    workerUrl?: string;
    accessToken?: () => Promise<string | null>;
    disconnectOnEmptyChannelsAfterMs?: number;
    /**
     * Storage compatible object used by the underlying socket for longpoll fallback history.
     * Provide a custom implementation in environments where reading `globalThis.sessionStorage`
     * throws (sandboxed iframes, in-app webviews, "block third-party storage" privacy modes).
     * Defaults to `globalThis.sessionStorage` when accessible, otherwise an in-memory store.
     */
    sessionStorage?: Storage;
};
export default class RealtimeClient {
    channels: RealtimeChannel[];
    accessTokenValue: string | null;
    accessToken: (() => Promise<string | null>) | null;
    apiKey: string | null;
    httpEndpoint: string;
    /** @deprecated headers cannot be set on websocket connections */
    headers?: {
        [key: string]: string;
    };
    params?: {
        [key: string]: string;
    };
    ref: number;
    logLevel?: LogLevel;
    fetch: Fetch;
    worker?: boolean;
    workerUrl?: string;
    workerRef?: Worker;
    serializer: Serializer;
    get endPoint(): string;
    get timeout(): number;
    get transport(): WebSocketLikeConstructor;
    get heartbeatCallback(): HeartbeatCallback;
    get heartbeatIntervalMs(): number;
    get heartbeatTimer(): HeartbeatTimer;
    get pendingHeartbeatRef(): string | null;
    get reconnectTimer(): Timer;
    get vsn(): Vsn;
    get encode(): Encode<void>;
    get decode(): Decode<void>;
    get reconnectAfterMs(): (tries: number) => number;
    get sendBuffer(): (() => void)[];
    get stateChangeCallbacks(): {
        open: [string, Function][];
        close: [string, Function][];
        error: [string, Function][];
        message: [string, Function][];
    };
    private _manuallySetToken;
    private _authPromise;
    private _authGeneration;
    private _workerHeartbeatTimer;
    private _pendingWorkerHeartbeatRef;
    private _pendingDisconnectTimer;
    private _disconnectOnEmptyChannelsAfterMs;
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
    constructor(endPoint: string, options?: RealtimeClientOptions);
    /**
     * Connects the socket, unless already connected.
     *
     * @category Realtime
     */
    connect(): void;
    /**
     * Returns the URL of the websocket.
     * @returns string The URL of the websocket.
     *
     * @category Realtime
     */
    endpointURL(): string;
    /**
     * Disconnects the socket.
     *
     * @param code A numeric status code to send on disconnect.
     * @param reason A custom reason for the disconnect.
     *
     * @category Realtime
     */
    disconnect(code?: number, reason?: string): Promise<"ok" | "timeout">;
    /**
     * Returns all created channels
     *
     * @category Realtime
     */
    getChannels(): RealtimeChannel[];
    /**
     * Unsubscribes, removes and tears down a single channel
     * @param channel A RealtimeChannel instance
     *
     * @category Realtime
     */
    removeChannel(channel: RealtimeChannel): Promise<RealtimeRemoveChannelResponse>;
    /**
     * Unsubscribes, removes and tears down all channels
     *
     * @category Realtime
     */
    removeAllChannels(): Promise<RealtimeRemoveChannelResponse[]>;
    /**
     * Logs the message.
     *
     * For customized logging, `this.logger` can be overridden in Client constructor.
     *
     * @category Realtime
     */
    log(kind: string, msg: string, data?: any): void;
    /**
     * Returns true if a custom `logger` has been configured on this client.
     *
     * @category Realtime
     */
    hasLogger(): boolean;
    /**
     * Returns the current state of the socket.
     *
     * @category Realtime
     */
    connectionState(): import("./lib/constants").ConnectionState;
    /**
     * Returns `true` is the connection is open.
     *
     * @category Realtime
     */
    isConnected(): boolean;
    /**
     * Returns `true` if the connection is currently connecting.
     *
     * @category Realtime
     */
    isConnecting(): boolean;
    /**
     * Returns `true` if the connection is currently disconnecting.
     *
     * @category Realtime
     */
    isDisconnecting(): boolean;
    /**
     * Creates (or reuses) a {@link RealtimeChannel} for the provided topic.
     *
     * Topics are automatically prefixed with `realtime:` to match the Realtime service.
     * If a channel with the same topic already exists it will be returned instead of creating
     * a duplicate connection.
     *
     * @category Realtime
     */
    channel(topic: string, params?: RealtimeChannelOptions): RealtimeChannel;
    /**
     * Push out a message if the socket is connected.
     *
     * If the socket is not connected, the message gets enqueued within a local buffer, and sent out when a connection is next established.
     *
     * @category Realtime
     */
    push(data: RealtimeMessage): void;
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
    setAuth(token?: string | null): Promise<void>;
    /**
     * Sends a heartbeat message if the socket is connected.
     *
     * @category Realtime
     */
    sendHeartbeat(): Promise<void>;
    /**
     * Sets a callback that receives lifecycle events for internal heartbeat messages.
     * Useful for instrumenting connection health (e.g. sent/ok/timeout).
     *
     * @category Realtime
     */
    onHeartbeat(callback: HeartbeatCallback): void;
}
export {};
//# sourceMappingURL=RealtimeClient.d.ts.map