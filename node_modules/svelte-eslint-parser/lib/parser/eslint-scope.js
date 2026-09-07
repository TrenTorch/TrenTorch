import { loadNewestModule } from "../utils/cjs-module.js";
import * as eslintScope from "eslint-scope";
let eslintScopeCache = null;
/**
 * Load `eslint-scope` from ESLint's dependencies, user dependencies, or this package's dependencies.
 * Return the latest version among them.
 */
export function getESLintScope() {
    if (!eslintScopeCache) {
        try {
            eslintScopeCache = loadNewestModule("eslint-scope");
        }
        catch {
            // ignore
        }
        if (!eslintScopeCache) {
            eslintScopeCache = eslintScope.default || eslintScope;
        }
    }
    return eslintScopeCache;
}
