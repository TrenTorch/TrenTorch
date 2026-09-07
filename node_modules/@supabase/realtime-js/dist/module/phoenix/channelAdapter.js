import { CHANNEL_STATES, MAX_PUSH_BUFFER_SIZE } from '../lib/constants';
export default class ChannelAdapter {
    constructor(socket, topic, params) {
        const phoenixParams = phoenixChannelParams(params);
        this.channel = socket.getSocket().channel(topic, phoenixParams);
        this.socket = socket;
    }
    get state() {
        return this.channel.state;
    }
    set state(state) {
        this.channel.state = state;
    }
    get joinedOnce() {
        return this.channel.joinedOnce;
    }
    get joinPush() {
        return this.channel.joinPush;
    }
    get rejoinTimer() {
        return this.channel.rejoinTimer;
    }
    on(event, callback) {
        return this.channel.on(event, callback);
    }
    off(event, refNumber) {
        this.channel.off(event, refNumber);
    }
    subscribe(timeout) {
        return this.channel.join(timeout);
    }
    unsubscribe(timeout) {
        return this.channel.leave(timeout);
    }
    teardown() {
        this.channel.teardown();
    }
    onClose(callback) {
        this.channel.onClose(callback);
    }
    onError(callback) {
        return this.channel.onError(callback);
    }
    push(event, payload, timeout) {
        let push;
        try {
            push = this.channel.push(event, payload, timeout);
        }
        catch (error) {
            throw new Error(`tried to push '${event}' to '${this.channel.topic}' before joining. Use channel.subscribe() before pushing events`);
        }
        if (this.channel.pushBuffer.length > MAX_PUSH_BUFFER_SIZE) {
            const removedPush = this.channel.pushBuffer.shift();
            removedPush.cancelTimeout();
            this.socket.log('channel', `discarded push due to buffer overflow: ${removedPush.event}`, removedPush.payload());
        }
        return push;
    }
    updateJoinPayload(payload) {
        const oldPayload = this.channel.joinPush.payload();
        this.channel.joinPush.payload = () => (Object.assign(Object.assign({}, oldPayload), payload));
    }
    canPush() {
        return this.socket.isConnected() && this.state === CHANNEL_STATES.joined;
    }
    isJoined() {
        return this.state === CHANNEL_STATES.joined;
    }
    isJoining() {
        return this.state === CHANNEL_STATES.joining;
    }
    isClosed() {
        return this.state === CHANNEL_STATES.closed;
    }
    isLeaving() {
        return this.state === CHANNEL_STATES.leaving;
    }
    updateFilterBindings(filterBindings) {
        this.channel.filterBindings = filterBindings;
    }
    updatePayloadTransform(callback) {
        this.channel.onMessage = callback;
    }
    /**
     * @internal
     */
    getChannel() {
        return this.channel;
    }
}
function phoenixChannelParams(options) {
    return {
        config: Object.assign({
            broadcast: { ack: false, self: false },
            presence: { key: '', enabled: false },
            private: false,
        }, options.config),
    };
}
//# sourceMappingURL=channelAdapter.js.map