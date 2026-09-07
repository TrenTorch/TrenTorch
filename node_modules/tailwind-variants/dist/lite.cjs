'use strict';

var chunkHIKWJRSK_cjs = require('./chunk-HIKWJRSK.cjs');
var chunk2BFDQGZN_cjs = require('./chunk-2BFDQGZN.cjs');

// src/lite.ts
var cn = (...classnames) => {
  return (_config) => {
    const base = chunk2BFDQGZN_cjs.cx(classnames);
    return base || void 0;
  };
};
var cnAdapter = cn;
var classAdapter = (_config, ...classnames) => {
  const result = chunk2BFDQGZN_cjs.cx(classnames);
  return result || void 0;
};
var runtime = chunkHIKWJRSK_cjs.getTailwindVariants(classAdapter);
var tv = runtime.tv;
var createTV = runtime.createTV;
var defaultConfig2 = chunkHIKWJRSK_cjs.defaultConfig;

Object.defineProperty(exports, "cx", {
  enumerable: true,
  get: function () { return chunk2BFDQGZN_cjs.cx; }
});
exports.cn = cn;
exports.cnAdapter = cnAdapter;
exports.createTV = createTV;
exports.defaultConfig = defaultConfig2;
exports.tv = tv;
