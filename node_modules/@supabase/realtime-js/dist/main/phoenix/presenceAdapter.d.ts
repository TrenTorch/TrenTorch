import type { PresenceState, PresenceStates } from './types';
import type { RealtimePresenceOptions, RealtimePresenceState } from '../RealtimePresence';
import ChannelAdapter from './channelAdapter';
export default class PresenceAdapter {
    private presence;
    constructor(channel: ChannelAdapter, opts?: RealtimePresenceOptions);
    get state(): RealtimePresenceState;
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
    static transformState(state: PresenceStates): RealtimePresenceState;
    static onJoinPayload(key: string, currentPresence: PresenceState, newPresence: PresenceState): {
        event: string;
        key: string;
        currentPresences: {
            presence_ref: string;
        }[];
        newPresences: {
            presence_ref: string;
        }[];
    };
    static onLeavePayload(key: string, currentPresence: PresenceState, leftPresence: PresenceState): {
        event: string;
        key: string;
        currentPresences: {
            presence_ref: string;
        }[];
        leftPresences: {
            presence_ref: string;
        }[];
    };
}
//# sourceMappingURL=presenceAdapter.d.ts.map