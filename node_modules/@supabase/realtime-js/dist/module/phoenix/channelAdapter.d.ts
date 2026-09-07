import type { RealtimeChannelOptions } from '../RealtimeChannel';
import SocketAdapter from './socketAdapter';
import type { ChannelBindingCallback, ChannelOnMessage, ChannelOnErrorCallback, ChannelFilterBindings, ChannelState, Push, Timer } from './types';
export default class ChannelAdapter {
    private channel;
    private socket;
    constructor(socket: SocketAdapter, topic: string, params: RealtimeChannelOptions);
    get state(): ChannelState;
    set state(state: ChannelState);
    get joinedOnce(): boolean;
    get joinPush(): Push;
    get rejoinTimer(): Timer;
    on(event: string, callback: ChannelBindingCallback): number;
    off(event: string, refNumber?: number): void;
    subscribe(timeout?: number): Push;
    unsubscribe(timeout?: number): Push;
    teardown(): void;
    onClose(callback: ChannelBindingCallback): void;
    onError(callback: ChannelOnErrorCallback): number;
    push(event: string, payload: {
        [key: string]: any;
    }, timeout?: number): Push;
    updateJoinPayload(payload: Record<string, any>): void;
    canPush(): boolean;
    isJoined(): boolean;
    isJoining(): boolean;
    isClosed(): boolean;
    isLeaving(): boolean;
    updateFilterBindings(filterBindings: ChannelFilterBindings): void;
    updatePayloadTransform(callback: ChannelOnMessage): void;
}
//# sourceMappingURL=channelAdapter.d.ts.map