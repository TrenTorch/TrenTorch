import { getTailwindVariants, defaultConfig } from './chunk-SUL6UUW2.js';
import { cx } from './chunk-OYFAXDFZ.js';
export { cx } from './chunk-OYFAXDFZ.js';

// src/lite.ts
var cn = (...classnames) => {
  return (_config) => {
    const base = cx(classnames);
    return base || void 0;
  };
};
var cnAdapter = cn;
var classAdapter = (_config, ...classnames) => {
  const result = cx(classnames);
  return result || void 0;
};
var runtime = getTailwindVariants(classAdapter);
var tv = runtime.tv;
var createTV = runtime.createTV;
var defaultConfig2 = defaultConfig;

export { cn, cnAdapter, createTV, defaultConfig2 as defaultConfig, tv };
