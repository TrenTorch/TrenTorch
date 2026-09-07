import type { NormalizedParserOptions } from "./parser/parser-options.js";
interface TsLike {
    sys?: {
        readFile?: (path: string, encoding?: string) => string | undefined;
    };
}
/** Called from `parseForESLint` so translation has the user's parser config. */
export declare function rememberParserOptions(options: NormalizedParserOptions): void;
/** Seed the cache so a later `ts.sys.readFile` skips re-translating. */
export declare function primeTranslationCache(filePath: string, virtualCode: string): void;
/** Idempotent. No-op unless `SVELTE_ESLINT_PARSER_EXPERIMENTAL_TS_SYS_HOOK=1`. */
export declare function installTsSysHook(): void;
/** Test seam. The `ts.sys` patches themselves are intentionally permanent. */
export declare function _resetTranslationCacheForTesting(): void;
/** Test seam: patch a caller-supplied `sys` instead of the require.cache ones. */
export declare function _patchTsSysForTesting(sys: TsLike["sys"]): void;
export {};
