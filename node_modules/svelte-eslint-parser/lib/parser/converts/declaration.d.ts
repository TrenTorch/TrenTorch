import type { SvelteDeclarationTag, SvelteElement, SvelteElseBlockAlone, SvelteAwaitCatchBlock, SvelteAwaitPendingBlock, SvelteAwaitThenBlock, SvelteEachBlock, SvelteIfBlock, SvelteKeyBlock, SvelteProgram, SvelteSnippetBlock } from "../../ast/index.js";
import type { Context } from "../../context/index.js";
import type * as Compiler from "../svelte-ast-types-for-v5.js";
/** Convert for DeclarationTag */
export declare function convertDeclarationTag(node: Compiler.DeclarationTag, parent: SvelteProgram | SvelteElement | SvelteIfBlock | SvelteElseBlockAlone | SvelteEachBlock | SvelteAwaitPendingBlock | SvelteAwaitThenBlock | SvelteAwaitCatchBlock | SvelteKeyBlock | SvelteSnippetBlock, ctx: Context): SvelteDeclarationTag;
