import type { ChannelState } from './lib/constants';
import type RealtimeClient from './RealtimeClient';
import RealtimePresence, { REALTIME_PRESENCE_LISTEN_EVENTS } from './RealtimePresence';
import type { RealtimePresenceJoinPayload, RealtimePresenceLeavePayload, RealtimePresenceState } from './RealtimePresence';
import { ChannelBindingCallback } from './phoenix/types';
import type { Timer } from './phoenix/types';
import { RealtimePostgresFilterBuilder } from './RealtimePostgresFilterBuilder';
export type { RealtimePostgresChangesFilterOperator } from './RealtimePostgresFilterBuilder';
export { RealtimePostgresFilterBuilder, postgresChangesFilter, } from './RealtimePostgresFilterBuilder';
type ReplayOption = {
    since: number;
    limit?: number;
};
export type RealtimeChannelOptions = {
    config: {
        /**
         * self option enables client to receive message it broadcast
         * ack option instructs server to acknowledge that broadcast message was received
         * replay option instructs server to replay broadcast messages
         * replication_ready option instructs the server to emit a `system` event once the
         * Postgres replication connection backing this channel is established and ready to
         * stream changes. Listen for it with `channel.on('system', {}, (payload) => ...)`;
         * the payload's `status` is `'ok'` (`message: 'Replication connection established'`)
         * on success or `'error'` if the connection is not ready in time.
         */
        broadcast?: {
            self?: boolean;
            ack?: boolean;
            replay?: ReplayOption;
            replication_ready?: boolean;
        };
        /**
         * key option is used to track presence payload across clients
         *
         * enabled controls whether this client receives presence state and updates from other
         * clients — set it to true (or add an `.on('presence', ...)` listener, which enables it
         * automatically) if you want to see who else is present. Without it, this client's
         * `presenceState()` stays empty and no `presence` events fire for you, because the
         * underlying presence state machine buffers incoming updates until it has received an
         * initial snapshot, which is only requested when this flag is set.
         *
         * It does not gate the other direction: calling `track()` always makes this client
         * visible to other subscribers that have presence enabled, regardless of this client's
         * own `enabled` setting. On RLS-protected (private) channels, receiving presence updates
         * additionally requires the `presence.read` policy to authorize this client.
         */
        presence?: {
            key?: string;
            enabled?: boolean;
        };
        /**
         * defines if the channel is private or not and if RLS policies will be used to check data
         */
        private?: boolean;
        /**
         * By default, `subscribe()` reports `SUBSCRIBED` as soon as the channel itself has joined,
         * which can happen before the server has actually established the `postgres_changes`
         * subscription (e.g. before the replication slot is streaming). Set `wait: true` to instead
         * hold the `SUBSCRIBED` callback until the server confirms the postgres_changes subscription
         * is active.
         *
         * If the subscription cannot be established, the server rejects the join and `subscribe()`
         * reports `CHANNEL_ERROR` with the server's reason (e.g.
         * `PostgresChangesSubscribeTimeout: ...` when the wait ran out, or
         * `RealtimeDisabledForConfiguration: ...` when the table is not enabled for Realtime).
         *
         * Has no effect on a channel with no `postgres_changes` bindings.
         *
         * Setting `wait: true` automatically extends the channel's join timeout so it outlasts the
         * server's held reply, so you don't need to pass a larger `timeout` to `subscribe()` yourself.
         * As a side effect of how Phoenix tracks the join timeout, other pushes on the channel that
         * do not pass an explicit timeout inherit the extended value too.
         */
        postgres_changes_options?: {
            wait?: boolean;
            /**
             * Milliseconds the server should wait for postgres_changes subscription confirmation when
             * `wait` is `true`. Defaults to 15000, and the server clamps it to its own configured
             * maximum (20s by default), so asking for more waits less.
             */
            timeout?: number;
        };
    };
};
type RealtimeChangesPayloadBase = {
    schema: string;
    table: string;
};
type RealtimeBroadcastChangesPayloadBase = RealtimeChangesPayloadBase & {
    id: string;
};
export type RealtimeBroadcastInsertPayload<T extends {
    [key: string]: any;
}> = RealtimeBroadcastChangesPayloadBase & {
    operation: `${REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.INSERT}`;
    record: T;
    old_record: null;
};
export type RealtimeBroadcastUpdatePayload<T extends {
    [key: string]: any;
}> = RealtimeBroadcastChangesPayloadBase & {
    operation: `${REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.UPDATE}`;
    record: T;
    old_record: T;
};
export type RealtimeBroadcastDeletePayload<T extends {
    [key: string]: any;
}> = RealtimeBroadcastChangesPayloadBase & {
    operation: `${REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.DELETE}`;
    record: null;
    old_record: T;
};
export type RealtimeBroadcastPayload<T extends {
    [key: string]: any;
}> = RealtimeBroadcastInsertPayload<T> | RealtimeBroadcastUpdatePayload<T> | RealtimeBroadcastDeletePayload<T>;
type RealtimePostgresChangesPayloadBase = {
    schema: string;
    table: string;
    commit_timestamp: string;
    errors: string[];
};
export type RealtimePostgresInsertPayload<T extends {
    [key: string]: any;
}> = RealtimePostgresChangesPayloadBase & {
    eventType: `${REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.INSERT}`;
    new: T;
    old: {};
};
export type RealtimePostgresUpdatePayload<T extends {
    [key: string]: any;
}> = RealtimePostgresChangesPayloadBase & {
    eventType: `${REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.UPDATE}`;
    new: T;
    old: Partial<T>;
};
export type RealtimePostgresDeletePayload<T extends {
    [key: string]: any;
}> = RealtimePostgresChangesPayloadBase & {
    eventType: `${REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.DELETE}`;
    new: {};
    old: Partial<T>;
};
export type RealtimePostgresChangesPayload<T extends {
    [key: string]: any;
}> = RealtimePostgresInsertPayload<T> | RealtimePostgresUpdatePayload<T> | RealtimePostgresDeletePayload<T>;
export type RealtimePostgresChangesFilter<T extends `${REALTIME_POSTGRES_CHANGES_LISTEN_EVENT}`> = {
    /**
     * The type of database change to listen to.
     */
    event: T;
    /**
     * The database schema to listen to.
     */
    schema: string;
    /**
     * The database table to listen to.
     */
    table?: string;
    /**
     * Receive database changes only when the filter is matched.
     *
     * A filter is a `column=operator.value` expression, e.g. `id=eq.1` or
     * `title=like.%foo%`. See {@link RealtimePostgresChangesFilterOperator} for
     * the available operators.
     *
     * Multiple filters can be combined with commas; they are applied as an `AND`
     * condition: `filter: 'id=gt.0,id=lt.100'`.
     *
     * Any operator can be negated with the `not.` prefix: `filter: 'status=not.in.(draft,archived)'`.
     *
     * The server splits conditions on commas outside quotes/parentheses. To
     * include a reserved character (`,`, `(`, `)`) in a value, wrap it in double
     * quotes PostgREST-style: `name=eq."a,b"`. The {@link RealtimePostgresFilterBuilder}
     * does this quoting for you.
     *
     * Instead of a raw string you can pass a {@link RealtimePostgresFilterBuilder}
     * (via `postgresChangesFilter()`) for a type-checked, ergonomic way to compose filters; the
     * SDK serializes it to a string automatically.
     */
    filter?: string | RealtimePostgresFilterBuilder;
    /**
     * Restrict the change payload to a subset of columns instead of receiving the
     * full row. Reduces payload size (helpful for large `bytea`/`jsonb` columns)
     * and the data transferred per event.
     *
     * The listed columns must be selectable by the subscribing role.
     *
     * @example
     * channel.on('postgres_changes', {
     *   event: '*',
     *   schema: 'public',
     *   table: 'users',
     *   select: ['id', 'first_name'],
     * }, (payload) => {
     *   // payload.new only contains { id, first_name }
     * })
     */
    select?: string[];
};
export type RealtimeChannelSendResponse = 'ok' | 'timed out' | 'error' | (string & {});
/**
 * Payload of a `system` event emitted by the server.
 *
 * Most notably, when a channel is created with `config.broadcast.replication_ready: true`,
 * the server sends one of these once the Postgres replication connection is ready
 * (`status: 'ok'`) or fails to become ready in time (`status: 'error'`).
 */
export type RealtimeSystemPayload = {
    /** The extension that produced the message, e.g. `'system'` or `'postgres_changes'`. */
    extension: 'system' | 'postgres_changes' | (string & {});
    /** `'ok'` on success, `'error'` on failure. */
    status: 'ok' | 'error' | (string & {});
    /** Human-readable description, e.g. `'Replication connection established'`. */
    message: string;
    /** The channel (sub)topic the message refers to. */
    channel: string;
};
export declare enum REALTIME_POSTGRES_CHANGES_LISTEN_EVENT {
    ALL = "*",
    INSERT = "INSERT",
    UPDATE = "UPDATE",
    DELETE = "DELETE"
}
export declare enum REALTIME_LISTEN_TYPES {
    BROADCAST = "broadcast",
    PRESENCE = "presence",
    POSTGRES_CHANGES = "postgres_changes",
    SYSTEM = "system"
}
export declare enum REALTIME_SUBSCRIBE_STATES {
    SUBSCRIBED = "SUBSCRIBED",
    TIMED_OUT = "TIMED_OUT",
    CLOSED = "CLOSED",
    CHANNEL_ERROR = "CHANNEL_ERROR"
}
export declare const REALTIME_CHANNEL_STATES: {
    readonly closed: "closed";
    readonly errored: "errored";
    readonly joined: "joined";
    readonly joining: "joining";
    readonly leaving: "leaving";
};
type Binding = {
    type: string;
    filter: {
        [key: string]: any;
    };
    callback: ChannelBindingCallback;
    ref: number;
    id?: string;
};
/** A channel is the basic building block of Realtime
 * and narrows the scope of data flow to subscribed clients.
 * You can think of a channel as a chatroom where participants are able to see who's online
 * and send and receive messages.
 */
export default class RealtimeChannel {
    /** Topic name can be any string. */
    topic: string;
    params: RealtimeChannelOptions;
    socket: RealtimeClient;
    bindings: Record<string, Binding[]>;
    subTopic: string;
    broadcastEndpointURL: string;
    private: boolean;
    presence: RealtimePresence;
    get state(): ChannelState;
    set state(state: ChannelState);
    get joinedOnce(): boolean;
    get timeout(): number;
    get joinPush(): import("@supabase/phoenix").Push;
    get rejoinTimer(): Timer;
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
    topic: string, params: RealtimeChannelOptions | undefined, socket: RealtimeClient);
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
    subscribe(callback?: (status: REALTIME_SUBSCRIBE_STATES, err?: Error) => void, timeout?: number): RealtimeChannel;
    private _updatePostgresBindings;
    /**
     * Returns the current presence state for this channel.
     *
     * The shape is a map keyed by presence key (for example a user id) where each entry contains the
     * tracked metadata for that user.
     *
     * @category Realtime
     */
    presenceState<T extends {
        [key: string]: any;
    } = {}>(): RealtimePresenceState<T>;
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
    track(payload: {
        [key: string]: any;
    }, opts?: {
        [key: string]: any;
    }): Promise<RealtimeChannelSendResponse>;
    /**
     * Removes the current presence state for this client.
     *
     * @category Realtime
     */
    untrack(opts?: {
        [key: string]: any;
    }): Promise<RealtimeChannelSendResponse>;
    /**
     * Listen for presence events on this channel — when peers join, leave, or
     * sync presence state.
     */
    on(type: `${REALTIME_LISTEN_TYPES.PRESENCE}`, filter: {
        event: `${REALTIME_PRESENCE_LISTEN_EVENTS.SYNC}`;
    }, callback: () => void): RealtimeChannel;
    on<T extends {
        [key: string]: any;
    }>(type: `${REALTIME_LISTEN_TYPES.PRESENCE}`, filter: {
        event: `${REALTIME_PRESENCE_LISTEN_EVENTS.JOIN}`;
    }, callback: (payload: RealtimePresenceJoinPayload<T>) => void): RealtimeChannel;
    on<T extends {
        [key: string]: any;
    }>(type: `${REALTIME_LISTEN_TYPES.PRESENCE}`, filter: {
        event: `${REALTIME_PRESENCE_LISTEN_EVENTS.LEAVE}`;
    }, callback: (payload: RealtimePresenceLeavePayload<T>) => void): RealtimeChannel;
    on<T extends {
        [key: string]: any;
    }>(type: `${REALTIME_LISTEN_TYPES.PRESENCE}`, filter: {
        event: '*';
    }, callback: (payload?: RealtimePresenceJoinPayload<T> | RealtimePresenceLeavePayload<T>) => void): RealtimeChannel;
    /**
     * Listen for Postgres database changes (insert / update / delete) streamed
     * over this channel.
     */
    on<T extends {
        [key: string]: any;
    }>(type: `${REALTIME_LISTEN_TYPES.POSTGRES_CHANGES}`, filter: RealtimePostgresChangesFilter<`${REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.ALL}`>, callback: (payload: RealtimePostgresChangesPayload<T>) => void): RealtimeChannel;
    on<T extends {
        [key: string]: any;
    }>(type: `${REALTIME_LISTEN_TYPES.POSTGRES_CHANGES}`, filter: RealtimePostgresChangesFilter<`${REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.INSERT}`>, callback: (payload: RealtimePostgresInsertPayload<T>) => void): RealtimeChannel;
    on<T extends {
        [key: string]: any;
    }>(type: `${REALTIME_LISTEN_TYPES.POSTGRES_CHANGES}`, filter: RealtimePostgresChangesFilter<`${REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.UPDATE}`>, callback: (payload: RealtimePostgresUpdatePayload<T>) => void): RealtimeChannel;
    on<T extends {
        [key: string]: any;
    }>(type: `${REALTIME_LISTEN_TYPES.POSTGRES_CHANGES}`, filter: RealtimePostgresChangesFilter<`${REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.DELETE}`>, callback: (payload: RealtimePostgresDeletePayload<T>) => void): RealtimeChannel;
    on<T extends {
        [key: string]: any;
    }>(type: `${REALTIME_LISTEN_TYPES.POSTGRES_CHANGES}`, filter: RealtimePostgresChangesFilter<`${REALTIME_POSTGRES_CHANGES_LISTEN_EVENT}`>, callback: (payload: RealtimePostgresChangesPayload<T>) => void): RealtimeChannel;
    /**
     * Listen for broadcast messages sent on this channel.
     *
     * @param type One of "broadcast", "presence", or "postgres_changes".
     * @param filter Custom object specific to the Realtime feature detailing which payloads to receive.
     * @param callback Function to be invoked when event handler is triggered.
     */
    on(type: `${REALTIME_LISTEN_TYPES.BROADCAST}`, filter: {
        event: string;
    }, callback: (payload: {
        type: `${REALTIME_LISTEN_TYPES.BROADCAST}`;
        event: string;
        meta?: {
            replayed?: boolean;
            id: string;
        };
        [key: string]: any;
    }) => void): RealtimeChannel;
    on<T extends {
        [key: string]: any;
    }>(type: `${REALTIME_LISTEN_TYPES.BROADCAST}`, filter: {
        event: string;
    }, callback: (payload: {
        type: `${REALTIME_LISTEN_TYPES.BROADCAST}`;
        event: string;
        meta?: {
            replayed?: boolean;
            id: string;
        };
        payload: T;
    }) => void): RealtimeChannel;
    on<T extends Record<string, unknown>>(type: `${REALTIME_LISTEN_TYPES.BROADCAST}`, filter: {
        event: REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.ALL;
    }, callback: (payload: {
        type: `${REALTIME_LISTEN_TYPES.BROADCAST}`;
        event: REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.ALL;
        payload: RealtimeBroadcastPayload<T>;
    }) => void): RealtimeChannel;
    on<T extends {
        [key: string]: any;
    }>(type: `${REALTIME_LISTEN_TYPES.BROADCAST}`, filter: {
        event: REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.INSERT;
    }, callback: (payload: {
        type: `${REALTIME_LISTEN_TYPES.BROADCAST}`;
        event: REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.INSERT;
        payload: RealtimeBroadcastInsertPayload<T>;
    }) => void): RealtimeChannel;
    on<T extends {
        [key: string]: any;
    }>(type: `${REALTIME_LISTEN_TYPES.BROADCAST}`, filter: {
        event: REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.UPDATE;
    }, callback: (payload: {
        type: `${REALTIME_LISTEN_TYPES.BROADCAST}`;
        event: REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.UPDATE;
        payload: RealtimeBroadcastUpdatePayload<T>;
    }) => void): RealtimeChannel;
    on<T extends {
        [key: string]: any;
    }>(type: `${REALTIME_LISTEN_TYPES.BROADCAST}`, filter: {
        event: REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.DELETE;
    }, callback: (payload: {
        type: `${REALTIME_LISTEN_TYPES.BROADCAST}`;
        event: REALTIME_POSTGRES_CHANGES_LISTEN_EVENT.DELETE;
        payload: RealtimeBroadcastDeletePayload<T>;
    }) => void): RealtimeChannel;
    /**
     * Listen for `system` events on this channel.
     *
     * The payload follows the {@link RealtimeSystemPayload} shape. Opt in to the replication-ready
     * notification with `config.broadcast.replication_ready: true` when creating the channel, then
     * watch for `payload.status === 'ok'` to know the Postgres replication connection is ready.
     *
     * @example Know when the replication connection is ready
     * ```js
     * const channel = supabase.channel('room1', {
     *   config: { broadcast: { replication_ready: true } },
     * })
     *
     * channel
     *   .on('postgres_changes', { event: '*', schema: 'public', table: 'messages' }, (payload) => {
     *     console.log('Change received!', payload)
     *   })
     *   .on('system', {}, (payload) => {
     *     if (payload.extension === 'system' && payload.status === 'ok') {
     *       console.log('Replication connection is ready:', payload.message)
     *     }
     *   })
     *   .subscribe()
     * ```
     */
    on<T extends {
        [key: string]: any;
    }>(type: `${REALTIME_LISTEN_TYPES.SYSTEM}`, filter: {}, callback: (payload: any) => void): RealtimeChannel;
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
    httpSend(event: string, payload: any, opts?: {
        timeout?: number;
    }): Promise<{
        success: true;
    } | {
        success: false;
        status: number;
        error: string;
    }>;
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
    send(args: {
        type: 'broadcast' | 'presence' | 'postgres_changes';
        event: string;
        payload?: any;
        [key: string]: any;
    }, opts?: {
        [key: string]: any;
    }): Promise<RealtimeChannelSendResponse>;
    /**
     * Updates the payload that will be sent the next time the channel joins (reconnects).
     * Useful for rotating access tokens or updating config without re-creating the channel.
     *
     * @category Realtime
     */
    updateJoinPayload(payload: Record<string, any>): void;
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
    unsubscribe(timeout?: number): Promise<RealtimeChannelSendResponse>;
    /**
     * Destroys and stops related timers.
     *
     * @category Realtime
     */
    teardown(): void;
    copyBindings(other: RealtimeChannel): void;
}
//# sourceMappingURL=RealtimeChannel.d.ts.map