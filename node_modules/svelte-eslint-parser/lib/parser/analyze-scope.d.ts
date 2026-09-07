import type ESTree from "estree";
import type * as eslint from "eslint";
import type { SvelteScriptElement, SvelteSnippetBlock } from "../ast/index.js";
import type { NormalizedParserOptions } from "./parser-options.js";
import type { SvelteParseContext } from "./svelte-parse-context.js";
/**
 * Analyze scope
 */
export declare function analyzeScope(node: ESTree.Node, parserOptions: NormalizedParserOptions): eslint.Scope.ScopeManager;
/** Analyze reactive scope */
export declare function analyzeReactiveScope(scopeManager: eslint.Scope.ScopeManager): void;
/**
 * Analyze store scope. e.g. $count
 */
export declare function analyzeStoreScope(scopeManager: eslint.Scope.ScopeManager, svelteParseContext: SvelteParseContext): void;
/** Transform props exports */
export declare function analyzePropsScope(body: SvelteScriptElement, scopeManager: eslint.Scope.ScopeManager, svelteParseContext: SvelteParseContext): void;
/** Analyze snippets in component scope */
export declare function analyzeSnippetsScope(snippets: SvelteSnippetBlock[], scopeManager: eslint.Scope.ScopeManager): void;
