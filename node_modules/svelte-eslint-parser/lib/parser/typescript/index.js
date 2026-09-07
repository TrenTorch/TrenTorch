import { parseScript, parseScriptInSvelte } from "../script.js";
import { analyzeTypeScript, analyzeTypeScriptInSvelte, } from "./analyze/index.js";
import { setParent } from "./set-parent.js";
import { primeTranslationCache } from "../../ts-sys-hook.js";
/**
 * Parse for TypeScript in <script>
 */
export function parseTypeScriptInSvelte(code, attrs, parserOptions, context) {
    const tsCtx = analyzeTypeScriptInSvelte(code, attrs, parserOptions, context);
    // Share the shim with the ts.sys hook so projectService reads hit a cache.
    if (parserOptions.filePath) {
        primeTranslationCache(parserOptions.filePath, tsCtx.script);
    }
    const result = parseScriptInSvelte(tsCtx.script, attrs, parserOptions);
    tsCtx.restoreContext.restore(result);
    return result;
}
/**
 * Parse for TypeScript
 */
export function parseTypeScript(code, attrs, parserOptions, svelteParseContext) {
    const tsCtx = analyzeTypeScript(code, attrs, parserOptions, svelteParseContext);
    const result = parseScript(tsCtx.script, attrs, parserOptions);
    setParent(result);
    tsCtx.restoreContext.restore(result);
    return result;
}
