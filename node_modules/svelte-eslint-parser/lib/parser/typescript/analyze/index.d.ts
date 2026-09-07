import { VirtualTypeScriptContext } from "../context.js";
import type { SvelteHTMLElement } from "../../../ast/index.js";
import type { NormalizedParserOptions } from "../../parser-options.js";
import type { SvelteParseContext } from "../../svelte-parse-context.js";
export type AnalyzeTypeScriptContext = {
    slots: Set<SvelteHTMLElement>;
    svelteParseContext: SvelteParseContext;
};
type SvelteTypeScriptCode = {
    /**
     * User-authored <script> content.
     *
     * Example:
     *   <script lang="ts">
     *     const x = $derived(0);
     *   </script>
     */
    script: string;
    /**
     * Template code that is wrapped in the synthetic render function, where
     * template scopes are modeled.
     *
     * Example:
     *   {#if ok}
     *     {const x = $derived(0)}
     *   {/if}
     */
    render: string;
    /**
     * Template-generated code that must stay outside the render wrapper, such as
     * top-level snippets.
     *
     * Example:
     *   {#snippet s()}
     *     {const x = $derived(0)}
     *   {/snippet}
     */
    rootScope: string;
};
/**
 * Analyze TypeScript source code in Svelte.
 * Generate virtual code to provide correct type information for Svelte store reference names, scopes, and runes.
 * See https://github.com/sveltejs/svelte-eslint-parser/blob/main/docs/internal-mechanism.md#scope-types
 */
export declare function analyzeTypeScriptInSvelte(
/** Split virtual code generated from the Svelte component. */
code: SvelteTypeScriptCode, attrs: Record<string, string | undefined>, parserOptions: NormalizedParserOptions, context: AnalyzeTypeScriptContext): VirtualTypeScriptContext;
/**
 * Analyze TypeScript source code.
 * Generate virtual code to provide correct type information for Svelte runes.
 * See https://github.com/sveltejs/svelte-eslint-parser/blob/main/docs/internal-mechanism.md#scope-types
 */
export declare function analyzeTypeScript(code: string, attrs: Record<string, string | undefined>, parserOptions: NormalizedParserOptions, svelteParseContext: SvelteParseContext): VirtualTypeScriptContext;
export {};
