"use strict";
/*
  This file draws heavily from https://github.com/phoenixframework/phoenix/blob/d344ec0a732ab4ee204215b31de69cf4be72e3bf/assets/js/phoenix/presence.js
  License: https://github.com/phoenixframework/phoenix/blob/d344ec0a732ab4ee204215b31de69cf4be72e3bf/LICENSE.md
*/
Object.defineProperty(exports, "__esModule", { value: true });
exports.REALTIME_PRESENCE_LISTEN_EVENTS = void 0;
const tslib_1 = require("tslib");
const presenceAdapter_1 = tslib_1.__importDefault(require("./phoenix/presenceAdapter"));
var REALTIME_PRESENCE_LISTEN_EVENTS;
(function (REALTIME_PRESENCE_LISTEN_EVENTS) {
    REALTIME_PRESENCE_LISTEN_EVENTS["SYNC"] = "sync";
    REALTIME_PRESENCE_LISTEN_EVENTS["JOIN"] = "join";
    REALTIME_PRESENCE_LISTEN_EVENTS["LEAVE"] = "leave";
})(REALTIME_PRESENCE_LISTEN_EVENTS || (exports.REALTIME_PRESENCE_LISTEN_EVENTS = REALTIME_PRESENCE_LISTEN_EVENTS = {}));
class RealtimePresence {
    get state() {
        return this.presenceAdapter.state;
    }
    /**
     * Creates a Presence helper that keeps the local presence state in sync with the server.
     *
     * @param channel - The realtime channel to bind to.
     * @param opts - Optional custom event names, e.g. `{ events: { state: 'state', diff: 'diff' } }`.
     *
     * @category Realtime
     *
     * @example Example for a presence channel
     * ```ts
     * const presence = new RealtimePresence(channel)
     *
     * channel.on('presence', ({ event, key }) => {
     *   console.log(`Presence ${event} on ${key}`)
     * })
     * ```
     */
    constructor(channel, opts) {
        this.channel = channel;
        this.presenceAdapter = new presenceAdapter_1.default(this.channel.channelAdapter, opts);
    }
}
exports.default = RealtimePresence;
//# sourceMappingURL=RealtimePresence.js.map