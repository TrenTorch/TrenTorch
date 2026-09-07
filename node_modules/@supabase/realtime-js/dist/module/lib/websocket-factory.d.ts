export interface WebSocketLike {
    readonly CONNECTING: number;
    readonly OPEN: number;
    readonly CLOSING: number;
    readonly CLOSED: number;
    readonly readyState: number;
    readonly url: string;
    readonly protocol: string;
    /**
     * Closes the socket, optionally providing a close code and reason.
     */
    close(code?: number, reason?: string): void;
    /**
     * Sends data through the socket using the underlying implementation.
     */
    send(data: string | ArrayBufferLike | Blob | ArrayBufferView): void;
    onopen: ((this: any, ev: Event) => any) | null;
    onmessage: ((this: any, ev: MessageEvent) => any) | null;
    onclose: ((this: any, ev: CloseEvent) => any) | null;
    onerror: ((this: any, ev: Event) => any) | null;
    /**
     * Registers an event listener on the socket (compatible with browser WebSocket API).
     */
    addEventListener(type: string, listener: EventListener): void;
    /**
     * Removes a previously registered event listener.
     */
    removeEventListener(type: string, listener: EventListener): void;
    binaryType?: string;
    bufferedAmount?: number;
    extensions?: string;
    dispatchEvent?: (event: Event) => boolean;
}
export interface WebSocketEnvironment {
    type: 'native' | 'cloudflare' | 'unsupported';
    /** WebSocket constructor for this environment, if available. */
    wsConstructor?: typeof WebSocket;
    error?: string;
    workaround?: string;
}
/**
 * Utilities for creating WebSocket instances across runtimes.
 */
export declare class WebSocketFactory {
    /**
     * Static-only utility – prevent instantiation.
     */
    private constructor();
    private static detectEnvironment;
    /**
     * Returns the best available WebSocket constructor for the current runtime.
     *
     * @category Realtime
     *
     * @example Example with error handling
     * ```ts
     * try {
     *   const WS = WebSocketFactory.getWebSocketConstructor()
     *   const socket = new WS('wss://example.com/socket')
     * } catch (error) {
     *   console.error('WebSocket not available in this environment.', error)
     * }
     * ```
     */
    static getWebSocketConstructor(): typeof WebSocket;
    /**
     * Detects whether the runtime can establish WebSocket connections.
     *
     * @category Realtime
     *
     * @example Example in a Node.js script
     * ```ts
     * if (!WebSocketFactory.isWebSocketSupported()) {
     *   console.error('WebSockets are required for this script.')
     *   process.exitCode = 1
     * }
     * ```
     */
    static isWebSocketSupported(): boolean;
}
export default WebSocketFactory;
//# sourceMappingURL=websocket-factory.d.ts.map