import type RealtimeChannel from './RealtimeChannel';
export type Presence<T extends {
    [key: string]: any;
} = {}> = {
    presence_ref: string;
} & T;
export type RealtimePresenceState<T extends {
    [key: string]: any;
} = {}> = {
    [key: string]: Presence<T>[];
};
export type RealtimePresenceJoinPayload<T extends {
    [key: string]: any;
}> = {
    event: `${REALTIME_PRESENCE_LISTEN_EVENTS.JOIN}`;
    key: string;
    currentPresences: Presence<T>[];
    newPresences: Presence<T>[];
};
export type RealtimePresenceLeavePayload<T extends {
    [key: string]: any;
}> = {
    event: `${REALTIME_PRESENCE_LISTEN_EVENTS.LEAVE}`;
    key: string;
    currentPresences: Presence<T>[];
    leftPresences: Presence<T>[];
};
export declare enum REALTIME_PRESENCE_LISTEN_EVENTS {
    SYNC = "sync",
    JOIN = "join",
    LEAVE = "leave"
}
export type RealtimePresenceOptions = {
    events?: {
        state: string;
        diff: string;
    };
};
export default class RealtimePresence {
    channel: RealtimeChannel;
    get state(): RealtimePresenceState;
    private presenceAdapter;
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
    constructor(channel: RealtimeChannel, opts?: RealtimePresenceOptions);
}
//# sourceMappingURL=RealtimePresence.d.ts.map