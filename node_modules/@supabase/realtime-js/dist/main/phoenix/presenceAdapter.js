"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const phoenix_1 = require("@supabase/phoenix");
class PresenceAdapter {
    constructor(channel, opts) {
        const phoenixOptions = phoenixPresenceOptions(opts);
        this.presence = new phoenix_1.Presence(channel.getChannel(), phoenixOptions);
        this.presence.onJoin((key, currentPresence, newPresence) => {
            const onJoinPayload = PresenceAdapter.onJoinPayload(key, currentPresence, newPresence);
            channel.getChannel().trigger('presence', onJoinPayload);
        });
        this.presence.onLeave((key, currentPresence, leftPresence) => {
            const onLeavePayload = PresenceAdapter.onLeavePayload(key, currentPresence, leftPresence);
            channel.getChannel().trigger('presence', onLeavePayload);
        });
        this.presence.onSync(() => {
            channel.getChannel().trigger('presence', { event: 'sync' });
        });
    }
    get state() {
        return PresenceAdapter.transformState(this.presence.state);
    }
    /**
     * @private
     * Remove 'metas' key
     * Change 'phx_ref' to 'presence_ref'
     * Remove 'phx_ref' and 'phx_ref_prev'
     *
     * @example Transform state
     * // returns {
     *  abc123: [
     *    { presence_ref: '2', user_id: 1 },
     *    { presence_ref: '3', user_id: 2 }
     *  ]
     * }
     * RealtimePresence.transformState({
     *  abc123: {
     *    metas: [
     *      { phx_ref: '2', phx_ref_prev: '1' user_id: 1 },
     *      { phx_ref: '3', user_id: 2 }
     *    ]
     *  }
     * })
     *
     */
    static transformState(state) {
        state = cloneState(state);
        return Object.getOwnPropertyNames(state).reduce((newState, key) => {
            const presences = state[key];
            newState[key] = transformState(presences);
            return newState;
        }, {});
    }
    static onJoinPayload(key, currentPresence, newPresence) {
        const currentPresences = parseCurrentPresences(currentPresence);
        const newPresences = transformState(newPresence);
        return {
            event: 'join',
            key,
            currentPresences,
            newPresences,
        };
    }
    static onLeavePayload(key, currentPresence, leftPresence) {
        const currentPresences = parseCurrentPresences(currentPresence);
        const leftPresences = transformState(leftPresence);
        return {
            event: 'leave',
            key,
            currentPresences,
            leftPresences,
        };
    }
}
exports.default = PresenceAdapter;
function transformState(presences) {
    return presences.metas.map((presence) => {
        // Object spread compiles to Object.assign for ES2017, which treats __proto__ as a setter.
        const descriptors = Object.getOwnPropertyDescriptors(presence);
        const transformedPresence = Object.defineProperties({}, descriptors);
        transformedPresence['presence_ref'] = transformedPresence['phx_ref'];
        delete transformedPresence['phx_ref'];
        delete transformedPresence['phx_ref_prev'];
        return transformedPresence;
    });
}
function cloneState(state) {
    return JSON.parse(JSON.stringify(state));
}
function phoenixPresenceOptions(opts) {
    return (opts === null || opts === void 0 ? void 0 : opts.events) && { events: opts.events };
}
function parseCurrentPresences(currentPresences) {
    return (currentPresences === null || currentPresences === void 0 ? void 0 : currentPresences.metas) ? transformState(currentPresences) : [];
}
//# sourceMappingURL=presenceAdapter.js.map