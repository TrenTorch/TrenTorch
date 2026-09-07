export const resolveFetch = (customFetch) => {
    if (customFetch) {
        return (...args) => customFetch(...args);
    }
    return (...args) => fetch(...args);
};
//# sourceMappingURL=helper.js.map