"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.WebSocketFactory = void 0;
/**
 * Utilities for creating WebSocket instances across runtimes.
 */
class WebSocketFactory {
    /**
     * Static-only utility – prevent instantiation.
     */
    constructor() { }
    static detectEnvironment() {
        var _a;
        if (typeof WebSocket !== 'undefined') {
            return { type: 'native', wsConstructor: WebSocket };
        }
        const gt = globalThis;
        if (typeof globalThis !== 'undefined' && typeof gt.WebSocket !== 'undefined') {
            return { type: 'native', wsConstructor: gt.WebSocket };
        }
        const gl = typeof global !== 'undefined' ? global : undefined;
        if (gl && typeof gl.WebSocket !== 'undefined') {
            return { type: 'native', wsConstructor: gl.WebSocket };
        }
        if (typeof globalThis !== 'undefined' &&
            typeof gt.WebSocketPair !== 'undefined' &&
            typeof globalThis.WebSocket === 'undefined') {
            return {
                type: 'cloudflare',
                error: 'Cloudflare Workers detected. WebSocket clients are not supported in Cloudflare Workers.',
                workaround: 'Use Cloudflare Workers WebSocket API for server-side WebSocket handling, or deploy to a different runtime.',
            };
        }
        if ((typeof globalThis !== 'undefined' && gt.EdgeRuntime) ||
            (typeof navigator !== 'undefined' && ((_a = navigator.userAgent) === null || _a === void 0 ? void 0 : _a.includes('Vercel-Edge')))) {
            return {
                type: 'unsupported',
                error: 'Edge runtime detected (Vercel Edge/Netlify Edge). WebSockets are not supported in edge functions.',
                workaround: 'Use serverless functions or a different deployment target for WebSocket functionality.',
            };
        }
        // Use dynamic property access to avoid Next.js Edge Runtime static analysis warnings
        const _process = globalThis['process'];
        if (_process) {
            const processVersions = _process['versions'];
            if (processVersions && processVersions['node']) {
                // Reaching here means an earlier check did not find a native WebSocket,
                // so this Node.js process is missing the global WebSocket (Node.js 22+).
                return {
                    type: 'unsupported',
                    error: 'Node.js detected but native WebSocket not found.',
                    workaround: 'Ensure you are running Node.js 22+ or provide a WebSocket implementation via the transport option.',
                };
            }
        }
        return {
            type: 'unsupported',
            error: 'Unknown JavaScript runtime without WebSocket support.',
            workaround: "Ensure you're running in a supported environment (browser, Node.js, Deno) or provide a custom WebSocket implementation.",
        };
    }
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
    static getWebSocketConstructor() {
        const env = this.detectEnvironment();
        if (env.wsConstructor) {
            return env.wsConstructor;
        }
        let errorMessage = env.error || 'WebSocket not supported in this environment.';
        if (env.workaround) {
            errorMessage += `\n\nSuggested solution: ${env.workaround}`;
        }
        throw new Error(errorMessage);
    }
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
    static isWebSocketSupported() {
        try {
            const env = this.detectEnvironment();
            return env.type === 'native';
        }
        catch (_a) {
            return false;
        }
    }
}
exports.WebSocketFactory = WebSocketFactory;
exports.default = WebSocketFactory;
//# sourceMappingURL=websocket-factory.js.map