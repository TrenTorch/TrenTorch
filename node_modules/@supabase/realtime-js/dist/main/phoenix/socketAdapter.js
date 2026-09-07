"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const phoenix_1 = require("@supabase/phoenix");
const constants_1 = require("../lib/constants");
class SocketAdapter {
    constructor(endPoint, options) {
        this.socket = new phoenix_1.Socket(endPoint, options);
    }
    get timeout() {
        return this.socket.timeout;
    }
    get endPoint() {
        return this.socket.endPoint;
    }
    get transport() {
        return this.socket.transport;
    }
    get heartbeatIntervalMs() {
        return this.socket.heartbeatIntervalMs;
    }
    get heartbeatCallback() {
        return this.socket.heartbeatCallback;
    }
    set heartbeatCallback(callback) {
        this.socket.heartbeatCallback = callback;
    }
    get heartbeatTimer() {
        return this.socket.heartbeatTimer;
    }
    get pendingHeartbeatRef() {
        return this.socket.pendingHeartbeatRef;
    }
    get reconnectTimer() {
        return this.socket.reconnectTimer;
    }
    get vsn() {
        return this.socket.vsn;
    }
    get encode() {
        return this.socket.encode;
    }
    get decode() {
        return this.socket.decode;
    }
    get reconnectAfterMs() {
        return this.socket.reconnectAfterMs;
    }
    get sendBuffer() {
        return this.socket.sendBuffer;
    }
    get stateChangeCallbacks() {
        return this.socket.stateChangeCallbacks;
    }
    connect() {
        this.socket.connect();
    }
    disconnect(callback, code, reason, timeout = 10000) {
        return new Promise((resolve) => {
            setTimeout(() => resolve('timeout'), timeout);
            this.socket.disconnect(() => {
                callback();
                resolve('ok');
            }, code, reason);
        });
    }
    push(data) {
        this.socket.push(data);
    }
    log(kind, msg, data) {
        this.socket.log(kind, msg, data);
    }
    hasLogger() {
        return this.socket.hasLogger();
    }
    makeRef() {
        return this.socket.makeRef();
    }
    onOpen(callback) {
        this.socket.onOpen(callback);
    }
    onClose(callback) {
        this.socket.onClose(callback);
    }
    onError(callback) {
        this.socket.onError(callback);
    }
    onMessage(callback) {
        this.socket.onMessage(callback);
    }
    isConnected() {
        return this.socket.isConnected();
    }
    isConnecting() {
        return this.socket.connectionState() == constants_1.CONNECTION_STATE.connecting;
    }
    isDisconnecting() {
        return this.socket.connectionState() == constants_1.CONNECTION_STATE.closing;
    }
    connectionState() {
        // @ts-ignore - requires better typing and exposing type in phoenix
        return this.socket.connectionState();
    }
    endPointURL() {
        return this.socket.endPointURL();
    }
    sendHeartbeat() {
        this.socket.sendHeartbeat();
    }
    /**
     * @internal
     */
    getSocket() {
        return this.socket;
    }
}
exports.default = SocketAdapter;
//# sourceMappingURL=socketAdapter.js.map