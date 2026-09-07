"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.resolveFetch = void 0;
const resolveFetch = (customFetch) => {
    if (customFetch) {
        return (...args) => customFetch(...args);
    }
    return (...args) => fetch(...args);
};
exports.resolveFetch = resolveFetch;
//# sourceMappingURL=helper.js.map