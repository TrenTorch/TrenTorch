import './rule-types.js';
import { rules as ruleList } from './utils/rules.js';
import base from './configs/flat/base.js';
import recommended from './configs/flat/recommended.js';
import prettier from './configs/flat/prettier.js';
import all from './configs/flat/all.js';
import * as processor from './processor/index.js';
import * as metaModule from './meta.js';
/* eslint-disable @typescript-eslint/no-unnecessary-type-assertion -- ts(2742) Error */
export const configs = {
    base: base,
    recommended: recommended,
    prettier: prettier,
    all: all,
    // For backward compatibility
    'flat/base': base,
    'flat/recommended': recommended,
    'flat/prettier': prettier,
    'flat/all': all
};
/* eslint-enable @typescript-eslint/no-unnecessary-type-assertion -- ts(2742) Error */
export const rules = ruleList.reduce((obj, r) => {
    obj[r.meta.docs.ruleName] = r;
    return obj;
}, {});
export const meta = { ...metaModule };
export const processors = {
    '.svelte': processor,
    svelte: processor
};
