import type { SocketState, ChannelState, ChannelEvent as PhoenixChannelEvent, Transport, Vsn } from '../phoenix/types';
export type { SocketState, ChannelState, Transport };
export declare const DEFAULT_VERSION = "realtime-js/2.116.0";
export declare const VSN_1_0_0: Vsn;
export declare const VSN_2_0_0: Vsn;
export declare const DEFAULT_VSN: Vsn;
export declare const VERSION = "2.116.0";
export declare const DEFAULT_TIMEOUT = 10000;
/** Mirrors the Realtime server's own default for `postgres_changes_options.timeout`. */
export declare const DEFAULT_POSTGRES_CHANGES_WAIT_TIMEOUT = 15000;
/**
 * Headroom added to the join timeout when waiting on postgres_changes, covering the
 * CHANNEL_ERROR_BACKOFF_MS sleep (5s by default) the server takes before rejecting a join.
 */
export declare const POSTGRES_CHANGES_WAIT_ERROR_GRACE = 10000;
export declare const WS_CLOSE_NORMAL = 1000;
export declare const MAX_PUSH_BUFFER_SIZE = 100;
export declare const SOCKET_STATES: {
    readonly connecting: 0;
    readonly open: 1;
    readonly closing: 2;
    readonly closed: 3;
};
export declare const CHANNEL_STATES: {
    readonly closed: "closed";
    readonly errored: "errored";
    readonly joined: "joined";
    readonly joining: "joining";
    readonly leaving: "leaving";
};
export type ChannelEvent = PhoenixChannelEvent | 'access_token';
export declare const CHANNEL_EVENTS: {
    readonly close: "phx_close";
    readonly error: "phx_error";
    readonly join: "phx_join";
    readonly reply: "phx_reply";
    readonly leave: "phx_leave";
    readonly access_token: "access_token";
};
export declare const TRANSPORTS: {
    readonly websocket: "websocket";
};
export type ConnectionState = 'connecting' | 'open' | 'closing' | 'closed' | (string & {});
export declare const CONNECTION_STATE: {
    readonly connecting: "connecting";
    readonly open: "open";
    readonly closing: "closing";
    readonly closed: "closed";
};
//# sourceMappingURL=constants.d.ts.map