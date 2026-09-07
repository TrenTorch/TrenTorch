import type { NormalizedParserOptions } from "./parser-options.js";
/**
 * Translate a Svelte component to the virtual TypeScript shim. Returns
 * `null` if the file has no `<script lang="ts">` or parsing fails.
 */
export declare function svelteToVirtualTypeScript(filePath: string, content: string, parserOptions: NormalizedParserOptions): string | null;
