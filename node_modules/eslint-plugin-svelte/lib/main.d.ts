import './rule-types.js';
import * as processor from './processor/index.js';
import type { Linter, Rule } from 'eslint';
export declare const configs: {
    base: Linter.Config[];
    recommended: Linter.Config[];
    prettier: Linter.Config[];
    all: Linter.Config[];
    'flat/base': Linter.Config[];
    'flat/recommended': Linter.Config[];
    'flat/prettier': Linter.Config[];
    'flat/all': Linter.Config[];
};
export declare const rules: Record<string, Rule.RuleModule>;
export declare const meta: {
    name: "eslint-plugin-svelte";
    version: "3.23.0";
};
export declare const processors: {
    '.svelte': typeof processor;
    svelte: typeof processor;
};
