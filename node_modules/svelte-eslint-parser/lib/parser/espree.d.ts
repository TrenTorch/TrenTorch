import type { BasicParserObject } from "./parser-object.js";
/**
 * Load `espree` from ESLint's dependencies, user dependencies, or this package's dependencies.
 * Return the latest version among them.
 */
export declare function getEspree(): BasicParserObject & {
    latestEcmaVersion: number;
};
