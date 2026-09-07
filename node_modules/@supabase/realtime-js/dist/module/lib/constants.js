import { version } from './version';
export const DEFAULT_VERSION = `realtime-js/${version}`;
export const VSN_1_0_0 = '1.0.0';
export const VSN_2_0_0 = '2.0.0';
export const DEFAULT_VSN = VSN_2_0_0;
export const VERSION = version;
export const DEFAULT_TIMEOUT = 10000;
/** Mirrors the Realtime server's own default for `postgres_changes_options.timeout`. */
export const DEFAULT_POSTGRES_CHANGES_WAIT_TIMEOUT = 15000;
/**
 * Headroom added to the join timeout when waiting on postgres_changes, covering the
 * CHANNEL_ERROR_BACKOFF_MS sleep (5s by default) the server takes before rejecting a join.
 */
export const POSTGRES_CHANGES_WAIT_ERROR_GRACE = 10000;
export const WS_CLOSE_NORMAL = 1000;
export const MAX_PUSH_BUFFER_SIZE = 100;
export const SOCKET_STATES = {
    connecting: 0,
    open: 1,
    closing: 2,
    closed: 3,
};
export const CHANNEL_STATES = {
    closed: 'closed',
    errored: 'errored',
    joined: 'joined',
    joining: 'joining',
    leaving: 'leaving',
};
export const CHANNEL_EVENTS = {
    close: 'phx_close',
    error: 'phx_error',
    join: 'phx_join',
    reply: 'phx_reply',
    leave: 'phx_leave',
    access_token: 'access_token',
};
export const TRANSPORTS = {
    websocket: 'websocket',
};
export const CONNECTION_STATE = {
    connecting: 'connecting',
    open: 'open',
    closing: 'closing',
    closed: 'closed',
};
//# sourceMappingURL=constants.js.map