import * as eslintScope from "eslint-scope";
/**
 * Load `eslint-scope` from ESLint's dependencies, user dependencies, or this package's dependencies.
 * Return the latest version among them.
 */
export declare function getESLintScope(): typeof eslintScope;
