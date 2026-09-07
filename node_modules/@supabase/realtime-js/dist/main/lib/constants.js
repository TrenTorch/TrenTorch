"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CONNECTION_STATE = exports.TRANSPORTS = exports.CHANNEL_EVENTS = exports.CHANNEL_STATES = exports.SOCKET_STATES = exports.MAX_PUSH_BUFFER_SIZE = exports.WS_CLOSE_NORMAL = exports.POSTGRES_CHANGES_WAIT_ERROR_GRACE = exports.DEFAULT_POSTGRES_CHANGES_WAIT_TIMEOUT = exports.DEFAULT_TIMEOUT = exports.VERSION = exports.DEFAULT_VSN = exports.VSN_2_0_0 = exports.VSN_1_0_0 = exports.DEFAULT_VERSION = void 0;
const version_1 = require("./version");
exports.DEFAULT_VERSION = `realtime-js/${version_1.version}`;
exports.VSN_1_0_0 = '1.0.0';
exports.VSN_2_0_0 = '2.0.0';
exports.DEFAULT_VSN = exports.VSN_2_0_0;
exports.VERSION = version_1.version;
exports.DEFAULT_TIMEOUT = 10000;
/** Mirrors the Realtime server's own default for `postgres_changes_options.timeout`. */
exports.DEFAULT_POSTGRES_CHANGES_WAIT_TIMEOUT = 15000;
/**
 * Headroom added to the join timeout when waiting on postgres_changes, covering the
 * CHANNEL_ERROR_BACKOFF_MS sleep (5s by default) the server takes before rejecting a join.
 */
exports.POSTGRES_CHANGES_WAIT_ERROR_GRACE = 10000;
exports.WS_CLOSE_NORMAL = 1000;
exports.MAX_PUSH_BUFFER_SIZE = 100;
exports.SOCKET_STATES = {
    connecting: 0,
    open: 1,
    closing: 2,
    closed: 3,
};
exports.CHANNEL_STATES = {
    closed: 'closed',
    errored: 'errored',
    joined: 'joined',
    joining: 'joining',
    leaving: 'leaving',
};
exports.CHANNEL_EVENTS = {
    close: 'phx_close',
    error: 'phx_error',
    join: 'phx_join',
    reply: 'phx_reply',
    leave: 'phx_leave',
    access_token: 'access_token',
};
exports.TRANSPORTS = {
    websocket: 'websocket',
};
exports.CONNECTION_STATE = {
    connecting: 'connecting',
    open: 'open',
    closing: 'closing',
    closed: 'closed',
};
//# sourceMappingURL=constants.js.map