import type { Message, SocketOnClose, SocketOnMessage, SocketOnOpen, SocketOnError, SocketOptions, SocketStateChangeCallbacks, Vsn, Encode, Decode, HeartbeatCallback, Timer } from './types';
import { ConnectionState } from '../lib/constants';
import type { HeartbeatTimer, WebSocketLikeConstructor } from '../RealtimeClient';
export default class SocketAdapter {
    private socket;
    constructor(endPoint: string, options: SocketOptions);
    get timeout(): number;
    get endPoint(): string;
    get transport(): WebSocketLikeConstructor;
    get heartbeatIntervalMs(): number;
    get heartbeatCallback(): HeartbeatCallback;
    set heartbeatCallback(callback: HeartbeatCallback);
    get heartbeatTimer(): HeartbeatTimer;
    get pendingHeartbeatRef(): string | null;
    get reconnectTimer(): Timer;
    get vsn(): Vsn;
    get encode(): Encode<void>;
    get decode(): Decode<void>;
    get reconnectAfterMs(): (tries: number) => number;
    get sendBuffer(): (() => void)[];
    get stateChangeCallbacks(): SocketStateChangeCallbacks;
    connect(): void;
    disconnect(callback: () => void, code?: number, reason?: string, timeout?: number): Promise<'ok' | 'timeout'>;
    push(data: Message<Record<string, unknown>>): void;
    log(kind: string, msg: string, data?: any): void;
    hasLogger(): boolean;
    makeRef(): string;
    onOpen(callback: SocketOnOpen): void;
    onClose(callback: SocketOnClose): void;
    onError(callback: SocketOnError): void;
    onMessage(callback: SocketOnMessage): void;
    isConnected(): boolean;
    isConnecting(): boolean;
    isDisconnecting(): boolean;
    connectionState(): ConnectionState;
    endPointURL(): string;
    sendHeartbeat(): void;
}
//# sourceMappingURL=socketAdapter.d.ts.map