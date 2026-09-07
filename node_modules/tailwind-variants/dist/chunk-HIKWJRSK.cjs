'use strict';

var chunk2BFDQGZN_cjs = require('./chunk-2BFDQGZN.cjs');

// src/internal/default-config.ts
var defaultConfig = {
  twMerge: true,
  twMergeConfig: {}
};

// src/internal/cache.ts
var VARIANT_CACHE_LIMIT = 256;
var OVERRIDE_CACHE_LIMIT = 128;
var CACHE_MISS = /* @__PURE__ */ Symbol("tv-cache-miss");
var hasClassOverride = (props) => (props == null ? void 0 : props.class) != null && props.class !== "" || (props == null ? void 0 : props.className) != null && props.className !== "";
var serializeFingerprintValue = (value) => {
  if (value === void 0) return "";
  if (value === null) return "null";
  if (typeof value === "string") return value;
  if (typeof value === "boolean") return value ? "true" : "false";
  if (typeof value === "number") return value === 0 ? "0" : String(value);
  if (typeof value === "bigint") return String(value);
  const mapped = chunk2BFDQGZN_cjs.falsyToString(value);
  const mappedType = typeof mapped;
  if (mappedType === "string" || mappedType === "number" || mappedType === "boolean" || mappedType === "bigint") {
    return String(mapped);
  }
  if (mappedType === "object") {
    try {
      return JSON.stringify(mapped);
    } catch {
      return null;
    }
  }
  return null;
};
var appendSignatureValue = (out, value) => {
  if (value === void 0) return out;
  if (value === null) return out + "null";
  const type = typeof value;
  if (type === "string" || type === "number" || type === "boolean" || type === "bigint") {
    return out + String(value);
  }
  if (Array.isArray(value)) {
    return out + value.join("\0");
  }
  try {
    return out + JSON.stringify(value);
  } catch {
    return out + "?";
  }
};
var buildPropsFingerprint = (variantKeys, defaultVariants, props, slotProps) => {
  let fingerprint = "";
  const seen = /* @__PURE__ */ Object.create(null);
  for (let i = 0; i < variantKeys.length; i++) {
    const key = variantKeys[i];
    seen[key] = 1;
    let value = defaultVariants[key];
    if (props && props[key] !== void 0) value = props[key];
    const serialized = serializeFingerprintValue(value);
    if (serialized === null) return null;
    fingerprint += key + ":" + serialized + ";";
  }
  const extras = [];
  for (const key in defaultVariants) {
    if (key === "class" || key === "className" || seen[key]) continue;
    seen[key] = 1;
    extras.push(key);
  }
  if (props) {
    for (const key in props) {
      if (key === "class" || key === "className" || seen[key] || props[key] === void 0) continue;
      seen[key] = 1;
      extras.push(key);
    }
  }
  if (extras.length > 1) extras.sort();
  for (let i = 0; i < extras.length; i++) {
    const key = extras[i];
    let value = defaultVariants[key];
    if (props && props[key] !== void 0) value = props[key];
    const serialized = serializeFingerprintValue(value);
    if (serialized === null) return null;
    fingerprint += key + ":" + serialized + ";";
  }
  return fingerprint;
};
var buildCompoundsSignature = (compoundVariants, compoundSlots) => {
  let signature = "";
  for (let i = 0; i < compoundVariants.length; i++) {
    const { conditionKeys, source } = compoundVariants[i];
    for (let j = 0; j < conditionKeys.length; j++) {
      const key = conditionKeys[j];
      signature += key + "=";
      signature = appendSignatureValue(signature, source[key]);
      signature += ",";
    }
    signature += "c=";
    signature = appendSignatureValue(signature, source.class);
    signature += "|cn=";
    signature = appendSignatureValue(signature, source.className);
    signature += ";";
  }
  for (let i = 0; i < compoundSlots.length; i++) {
    const { conditionKeys, source } = compoundSlots[i];
    for (let j = 0; j < conditionKeys.length; j++) {
      const key = conditionKeys[j];
      signature += key + "=";
      signature = appendSignatureValue(signature, source[key]);
      signature += ",";
    }
    if (Array.isArray(source.slots)) {
      signature += "slots=" + source.slots.join(",") + ",";
    }
    signature += "c=";
    signature = appendSignatureValue(signature, source.class);
    signature += "|cn=";
    signature = appendSignatureValue(signature, source.className);
    signature += ";";
  }
  return signature;
};
var createBoundedCache = (limit = VARIANT_CACHE_LIMIT) => {
  let primary = /* @__PURE__ */ new Map();
  let secondary = null;
  return {
    get(key) {
      if (primary.has(key)) return primary.get(key);
      if (secondary == null ? void 0 : secondary.has(key)) {
        const value = secondary.get(key);
        primary.set(key, value);
        return value;
      }
      return CACHE_MISS;
    },
    set(key, value) {
      if (primary.size >= limit) {
        secondary = primary;
        primary = /* @__PURE__ */ new Map();
      }
      primary.set(key, value);
    }
  };
};
var createResultCache = (limit = VARIANT_CACHE_LIMIT) => {
  const cache = createBoundedCache(limit);
  return {
    get(key) {
      return cache.get(key);
    },
    set(key, value) {
      cache.set(key, value);
    }
  };
};
var createNestedOverrideCache = (limit = OVERRIDE_CACHE_LIMIT) => {
  let primary = /* @__PURE__ */ new Map();
  let secondary = null;
  let size = 0;
  return {
    get(coreKey, overrideKey) {
      const primaryInner = primary.get(coreKey);
      if (primaryInner) {
        const value = primaryInner.get(overrideKey);
        if (value !== void 0 || primaryInner.has(overrideKey)) return value;
      }
      if (secondary) {
        const secondaryInner = secondary.get(coreKey);
        if (secondaryInner) {
          const value = secondaryInner.get(overrideKey);
          if (value !== void 0 || secondaryInner.has(overrideKey)) {
            let promoteInner = primary.get(coreKey);
            if (!promoteInner) {
              promoteInner = /* @__PURE__ */ new Map();
              primary.set(coreKey, promoteInner);
            }
            if (!promoteInner.has(overrideKey)) size++;
            promoteInner.set(overrideKey, value);
            return value;
          }
        }
      }
      return CACHE_MISS;
    },
    set(coreKey, overrideKey, value) {
      if (size >= limit) {
        secondary = primary;
        primary = /* @__PURE__ */ new Map();
        size = 0;
      }
      let inner = primary.get(coreKey);
      if (!inner) {
        inner = /* @__PURE__ */ new Map();
        primary.set(coreKey, inner);
      }
      if (!inner.has(overrideKey)) size++;
      inner.set(overrideKey, value);
    }
  };
};
var createLazyOverrideMerge = (cn, config) => {
  let cache = null;
  return (core, props) => {
    if (!hasClassOverride(props)) return core;
    const classVal = props.class;
    const classNameVal = props.className;
    if (classVal != null && classVal !== "" && typeof classVal !== "string" || classNameVal != null && classNameVal !== "" && typeof classNameVal !== "string") {
      return cn(config, core, classVal, classNameVal);
    }
    cache ??= createNestedOverrideCache();
    const coreKey = core ?? "";
    const overrideKey = (typeof classVal === "string" ? classVal : "") + "\0" + (typeof classNameVal === "string" ? classNameVal : "");
    const cached = cache.get(coreKey, overrideKey);
    if (cached !== CACHE_MISS) return cached;
    const merged = cn(config, core, classVal, classNameVal);
    cache.set(coreKey, overrideKey, merged);
    return merged;
  };
};

// src/internal/state.ts
function createState() {
  let cachedTwMerge = null;
  let cachedTwMergeConfig = {};
  let didTwMergeConfigChange = false;
  return {
    get cachedTwMerge() {
      return cachedTwMerge;
    },
    set cachedTwMerge(value) {
      cachedTwMerge = value;
    },
    get cachedTwMergeConfig() {
      return cachedTwMergeConfig;
    },
    set cachedTwMergeConfig(value) {
      cachedTwMergeConfig = value;
    },
    get didTwMergeConfigChange() {
      return didTwMergeConfigChange;
    },
    set didTwMergeConfigChange(value) {
      didTwMergeConfigChange = value;
    },
    reset() {
      cachedTwMerge = null;
      cachedTwMergeConfig = {};
      didTwMergeConfigChange = false;
    }
  };
}
var state = createState();

// src/internal/resolve-options.ts
var synchronizeTwMergeConfig = (config) => {
  if (!chunk2BFDQGZN_cjs.isEmptyObject(config.twMergeConfig) && !chunk2BFDQGZN_cjs.isEqual(config.twMergeConfig, state.cachedTwMergeConfig)) {
    state.didTwMergeConfigChange = true;
    state.cachedTwMergeConfig = config.twMergeConfig;
  }
};
var compileVariants = (variants, variantKeys) => {
  const compiledVariants = [];
  for (let i = 0; i < variantKeys.length; i++) {
    const key = variantKeys[i];
    const values = variants[key];
    compiledVariants.push({ key, values, isEmpty: chunk2BFDQGZN_cjs.isEmptyObject(values) });
  }
  return compiledVariants;
};
var compileCompoundVariants = (compoundVariants) => {
  if (!Array.isArray(compoundVariants) || compoundVariants.length === 0) return [];
  const result = [];
  for (let i = 0; i < compoundVariants.length; i++) {
    const compoundVariant = compoundVariants[i];
    const conditionKeys = [];
    for (const key in compoundVariant) {
      if (key !== "class" && key !== "className") {
        conditionKeys.push(key);
      }
    }
    result.push({ conditionKeys, source: compoundVariant });
  }
  return result;
};
var compileCompoundSlots = (compoundSlots) => {
  if (!Array.isArray(compoundSlots) || compoundSlots.length === 0) return [];
  const result = [];
  for (let i = 0; i < compoundSlots.length; i++) {
    const compoundSlot = compoundSlots[i];
    const conditionKeys = [];
    for (const key in compoundSlot) {
      if (key !== "slots" && key !== "class" && key !== "className") {
        conditionKeys.push(key);
      }
    }
    result.push({ conditionKeys, source: compoundSlot });
  }
  return result;
};
var indexCompoundSlotsBySlot = (compiledCompoundSlots) => {
  const index = {};
  for (let i = 0; i < compiledCompoundSlots.length; i++) {
    const compoundSlot = compiledCompoundSlots[i];
    const slots = compoundSlot.source.slots;
    if (!Array.isArray(slots)) continue;
    for (let j = 0; j < slots.length; j++) {
      const slotKey = slots[j];
      if (!index[slotKey]) index[slotKey] = [];
      index[slotKey].push(compoundSlot);
    }
  }
  return index;
};
var resolveOptions = (options, configProp) => {
  const {
    extend = null,
    slots: slotProps = {},
    variants: variantsProps = {},
    compoundVariants: compoundVariantsProps = [],
    compoundSlots: compoundSlotsProps = [],
    defaultVariants: defaultVariantsProps = {}
  } = options;
  const config = { ...defaultConfig, ...configProp };
  const hasSlots = options.slots !== void 0;
  const base = (extend == null ? void 0 : extend.base) ? chunk2BFDQGZN_cjs.cx(extend.base, options == null ? void 0 : options.base) : options == null ? void 0 : options.base;
  const variants = (extend == null ? void 0 : extend.variants) && !chunk2BFDQGZN_cjs.isEmptyObject(extend.variants) ? chunk2BFDQGZN_cjs.mergeObjects(variantsProps, extend.variants) : variantsProps;
  const defaultVariants = (extend == null ? void 0 : extend.defaultVariants) && !chunk2BFDQGZN_cjs.isEmptyObject(extend.defaultVariants) ? { ...extend.defaultVariants, ...defaultVariantsProps } : defaultVariantsProps;
  synchronizeTwMergeConfig(config);
  const isExtendedSlotsEmpty = !(extend == null ? void 0 : extend.slots) || chunk2BFDQGZN_cjs.isEmptyObject(extend.slots);
  const componentBase = hasSlots ? isExtendedSlotsEmpty && (extend == null ? void 0 : extend.base) ? chunk2BFDQGZN_cjs.cx(options == null ? void 0 : options.base, extend.base) : typeof (options == null ? void 0 : options.base) === "string" || (options == null ? void 0 : options.base) == null ? options.base : chunk2BFDQGZN_cjs.cx(options.base) : void 0;
  const componentSlots = hasSlots ? {
    base: componentBase,
    ...slotProps
  } : {};
  const slots = isExtendedSlotsEmpty ? componentSlots : chunk2BFDQGZN_cjs.joinObjects(
    { ...extend == null ? void 0 : extend.slots },
    chunk2BFDQGZN_cjs.isEmptyObject(componentSlots) ? { base: options == null ? void 0 : options.base } : componentSlots
  );
  const compoundVariants = !(extend == null ? void 0 : extend.compoundVariants) || chunk2BFDQGZN_cjs.isEmptyObject(extend.compoundVariants) ? compoundVariantsProps : chunk2BFDQGZN_cjs.flatMergeArrays(extend == null ? void 0 : extend.compoundVariants, compoundVariantsProps);
  const compoundSlots = !(extend == null ? void 0 : extend.compoundSlots) || chunk2BFDQGZN_cjs.isEmptyObject(extend.compoundSlots) ? compoundSlotsProps : chunk2BFDQGZN_cjs.flatMergeArrays(extend == null ? void 0 : extend.compoundSlots, compoundSlotsProps);
  const variantKeys = Object.keys(variants);
  const deferredError = compoundVariants && !Array.isArray(compoundVariants) ? new TypeError(
    `The "compoundVariants" prop must be an array. Received: ${typeof compoundVariants}`
  ) : compoundSlots && !Array.isArray(compoundSlots) ? new TypeError(
    `The "compoundSlots" prop must be an array. Received: ${typeof compoundSlots}`
  ) : null;
  const mode = hasSlots || !isExtendedSlotsEmpty ? "slots" : variantKeys.length === 0 ? "plain" : "variants";
  return {
    config,
    extend,
    base,
    variants,
    defaultVariants,
    slots,
    compoundVariants,
    compoundSlots,
    compiledVariants: null,
    compiledCompoundVariants: null,
    compiledCompoundSlots: null,
    compiledCompoundSlotsBySlot: null,
    deferredError,
    mode,
    slotKeys: null,
    variantKeys
  };
};
var compileResolvedOptions = (resolved) => {
  if (resolved.compiledVariants !== null) return resolved;
  resolved.compiledVariants = compileVariants(resolved.variants, resolved.variantKeys);
  resolved.compiledCompoundVariants = compileCompoundVariants(resolved.compoundVariants);
  resolved.compiledCompoundSlots = compileCompoundSlots(resolved.compoundSlots);
  resolved.compiledCompoundSlotsBySlot = indexCompoundSlotsBySlot(resolved.compiledCompoundSlots);
  resolved.slotKeys = resolved.slots && typeof resolved.slots === "object" ? Object.keys(resolved.slots) : [];
  return resolved;
};

// src/internal/class-resolver.ts
var EMPTY_ARRAY = [];
var variantClassesScratch = [];
var compoundClassesScratch = [];
var compoundVariantBySlotScratch = [];
var compoundSlotClassesScratch = [];
var getCompleteProps = (defaultVariants, props, slotProps) => {
  const result = {};
  for (const key in defaultVariants) {
    result[key] = defaultVariants[key];
  }
  if (props) {
    for (const key in props) {
      if (props[key] !== void 0) result[key] = props[key];
    }
  }
  if (slotProps) {
    for (const key in slotProps) {
      if (slotProps[key] !== void 0) result[key] = slotProps[key];
    }
  }
  return result;
};
var isNullishOrFalse = (value) => value == null || value === false;
var matchesCompoundValue = (expected, actual) => {
  if (!Array.isArray(expected)) {
    return expected === actual || isNullishOrFalse(expected) && isNullishOrFalse(actual);
  }
  for (let i = 0; i < expected.length; i++) {
    const expectedValue = expected[i];
    if (expectedValue === actual || isNullishOrFalse(expectedValue) && isNullishOrFalse(actual)) {
      return true;
    }
  }
  return false;
};
var getVariantValue = (variant, defaultVariants, props, slotProps) => {
  if (variant.isEmpty) return null;
  const variantProp = (slotProps == null ? void 0 : slotProps[variant.key]) ?? (props == null ? void 0 : props[variant.key]);
  if (variantProp === null) return null;
  const variantKey = chunk2BFDQGZN_cjs.falsyToString(variantProp);
  if (typeof variantKey === "object") return null;
  const defaultVariantProp = defaultVariants == null ? void 0 : defaultVariants[variant.key];
  const key = variantKey != null ? variantKey : chunk2BFDQGZN_cjs.falsyToString(defaultVariantProp);
  return variant.values[key || "false"];
};
var matchesConditions = (compound, completeProps) => {
  const { conditionKeys, source } = compound;
  for (let i = 0; i < conditionKeys.length; i++) {
    const key = conditionKeys[i];
    if (!matchesCompoundValue(source[key], completeProps[key])) return false;
  }
  return true;
};
var pushCompoundClassForSlot = (result, slotKey, classValue) => {
  if (typeof classValue === "string") {
    if (slotKey === "base") result.push(classValue);
  } else if (classValue && typeof classValue === "object" && classValue[slotKey]) {
    result.push(classValue[slotKey]);
  }
};
var getVariantClassNames = (variants, defaultVariants, props) => {
  const result = variantClassesScratch;
  result.length = 0;
  for (let i = 0; i < variants.length; i++) {
    const value = getVariantValue(variants[i], defaultVariants, props);
    if (value) result.push(value);
  }
  return result;
};
var getVariantClassNamesBySlot = (slotKey, variants, defaultVariants, props, slotProps) => {
  const result = variantClassesScratch;
  result.length = 0;
  for (let i = 0; i < variants.length; i++) {
    const variantValue = getVariantValue(variants[i], defaultVariants, props, slotProps);
    const value = slotKey === "base" && typeof variantValue === "string" ? variantValue : variantValue && variantValue[slotKey];
    if (value) result.push(value);
  }
  return result;
};
var getCompoundVariantClasses = (compoundVariants, completeProps) => {
  const result = compoundClassesScratch;
  result.length = 0;
  for (let i = 0; i < compoundVariants.length; i++) {
    const compoundVariant = compoundVariants[i];
    if (!matchesConditions(compoundVariant, completeProps)) continue;
    if (compoundVariant.source.class) result.push(compoundVariant.source.class);
    if (compoundVariant.source.className) result.push(compoundVariant.source.className);
  }
  return result;
};
var getCompoundVariantClassesBySlot = (slotKey, compoundVariants, completeProps) => {
  const result = compoundVariantBySlotScratch;
  result.length = 0;
  for (let i = 0; i < compoundVariants.length; i++) {
    const compoundVariant = compoundVariants[i];
    if (!matchesConditions(compoundVariant, completeProps)) continue;
    pushCompoundClassForSlot(result, slotKey, compoundVariant.source.class);
    pushCompoundClassForSlot(result, slotKey, compoundVariant.source.className);
  }
  return result;
};
var getCompoundSlotClasses = (compoundSlotsForKey, completeProps) => {
  const result = compoundSlotClassesScratch;
  result.length = 0;
  for (let i = 0; i < compoundSlotsForKey.length; i++) {
    const compoundSlot = compoundSlotsForKey[i];
    if (!matchesConditions(compoundSlot, completeProps)) continue;
    if (compoundSlot.source.class) result.push(compoundSlot.source.class);
    if (compoundSlot.source.className) result.push(compoundSlot.source.className);
  }
  return result;
};
var createPlainResolver = (resolved, cn) => {
  const { base, config } = resolved;
  let core = CACHE_MISS;
  const mergeOverride = createLazyOverrideMerge(cn, config);
  return ((props) => {
    if (core === CACHE_MISS) {
      core = cn(config, base);
    }
    return mergeOverride(core, props);
  });
};
var createVariantResolver = (resolved, cn) => {
  const { base, config, defaultVariants, deferredError, variantKeys } = resolved;
  let compiledCompoundVariants = resolved.compiledCompoundVariants;
  let compiledVariants = resolved.compiledVariants;
  let compiledCompoundSlots = EMPTY_ARRAY;
  let cache = null;
  const mergeOverride = createLazyOverrideMerge(cn, config);
  let coldInvokesRemaining = 1;
  const computeCore = (props) => {
    const compoundClasses = compiledCompoundVariants.length > 0 ? getCompoundVariantClasses(
      compiledCompoundVariants,
      getCompleteProps(defaultVariants, props)
    ) : void 0;
    return cn(
      config,
      base,
      getVariantClassNames(compiledVariants, defaultVariants, props),
      compoundClasses
    );
  };
  return ((props) => {
    if (deferredError) throw deferredError;
    if (compiledVariants === null || compiledCompoundVariants === null) {
      compileResolvedOptions(resolved);
      compiledVariants = resolved.compiledVariants;
      compiledCompoundVariants = resolved.compiledCompoundVariants;
      compiledCompoundSlots = resolved.compiledCompoundSlots ?? EMPTY_ARRAY;
    }
    let core;
    if (coldInvokesRemaining > 0) {
      coldInvokesRemaining--;
      core = computeCore(props);
    } else {
      cache ??= createResultCache();
      const propsFingerprint = buildPropsFingerprint(variantKeys, defaultVariants, props);
      if (propsFingerprint !== null) {
        const compoundsSig = compiledCompoundVariants.length > 0 || compiledCompoundSlots.length > 0 ? buildCompoundsSignature(compiledCompoundVariants, compiledCompoundSlots) : "";
        const cacheKey = propsFingerprint + "#" + compoundsSig;
        const cached = cache.get(cacheKey);
        if (cached !== CACHE_MISS) {
          core = cached;
        } else {
          core = computeCore(props);
          cache.set(cacheKey, core);
        }
      } else {
        core = computeCore(props);
      }
    }
    return mergeOverride(core, props);
  });
};
var createSlotsResolver = (resolved, cn) => {
  const { config, defaultVariants, deferredError, slots, variantKeys } = resolved;
  let compoundVariants = null;
  let compoundSlots = null;
  let keys = null;
  let slotComputers = null;
  let hasCompounds = false;
  let mergeOverride = null;
  let parentCache = null;
  let coldParentInvokesRemaining = 1;
  const ensureCompiled = () => {
    if (keys !== null) return;
    if (resolved.compiledVariants === null || resolved.compiledCompoundVariants === null || resolved.compiledCompoundSlots === null || resolved.compiledCompoundSlotsBySlot === null || resolved.slotKeys === null) {
      compileResolvedOptions(resolved);
    }
    const variants = resolved.compiledVariants;
    compoundVariants = resolved.compiledCompoundVariants;
    compoundSlots = resolved.compiledCompoundSlots;
    const compoundSlotsBySlot = resolved.compiledCompoundSlotsBySlot;
    keys = resolved.slotKeys;
    hasCompounds = compoundVariants.length > 0 || compoundSlots.length > 0;
    mergeOverride = createLazyOverrideMerge(cn, config);
    const computers = new Array(keys.length);
    for (let i = 0; i < keys.length; i++) {
      const slotKey = keys[i];
      const compoundSlotsForKey = compoundSlotsBySlot[slotKey] ?? EMPTY_ARRAY;
      computers[i] = (propsRef, slotProps) => {
        const completeProps = hasCompounds ? getCompleteProps(defaultVariants, propsRef, slotProps) : void 0;
        const compoundVariantClasses = completeProps ? getCompoundVariantClassesBySlot(slotKey, compoundVariants, completeProps) : void 0;
        const compoundSlotClasses = completeProps ? getCompoundSlotClasses(compoundSlotsForKey, completeProps) : void 0;
        return cn(
          config,
          slots[slotKey],
          getVariantClassNamesBySlot(slotKey, variants, defaultVariants, propsRef, slotProps),
          compoundVariantClasses,
          compoundSlotClasses
        );
      };
    }
    slotComputers = computers;
  };
  const createSlotsResult = (props) => {
    const slotKeys = keys;
    const computers = slotComputers;
    const overrideMerge = mergeOverride;
    const result = {};
    for (let i = 0; i < slotKeys.length; i++) {
      const compute = computers[i];
      const core = compute(props);
      result[slotKeys[i]] = (slotProps) => {
        if (slotProps == null) return core;
        let hasVariantOverride = false;
        for (const key in slotProps) {
          if (key === "class" || key === "className") continue;
          if (slotProps[key] !== void 0) {
            hasVariantOverride = true;
            break;
          }
        }
        if (!hasVariantOverride) {
          return overrideMerge(core, slotProps);
        }
        return overrideMerge(compute(props, slotProps), slotProps);
      };
    }
    return result;
  };
  return ((props) => {
    if (deferredError) throw deferredError;
    ensureCompiled();
    if (coldParentInvokesRemaining > 0) {
      coldParentInvokesRemaining--;
      return createSlotsResult(props);
    }
    const propsFingerprint = buildPropsFingerprint(variantKeys, defaultVariants, props);
    if (propsFingerprint === null) {
      return createSlotsResult(props);
    }
    const compoundsSig = hasCompounds ? buildCompoundsSignature(compoundVariants, compoundSlots) : "";
    const cacheKey = propsFingerprint + "#" + compoundsSig;
    parentCache ??= createBoundedCache();
    const cached = parentCache.get(cacheKey);
    if (cached !== CACHE_MISS) return cached;
    const next = createSlotsResult(props);
    parentCache.set(cacheKey, next);
    return next;
  });
};
var createClassResolver = (resolved, cn) => {
  if (resolved.mode === "plain") return createPlainResolver(resolved, cn);
  let resolver;
  return ((props) => {
    resolver ??= resolved.mode === "slots" ? createSlotsResolver(resolved, cn) : createVariantResolver(resolved, cn);
    return resolver(props);
  });
};

// src/internal/tv.ts
var attachComponentMetadata = (component, resolved) => {
  component.variantKeys = resolved.variantKeys;
  component.extend = resolved.extend;
  component.base = resolved.base;
  component.slots = resolved.slots;
  component.variants = resolved.variants;
  component.defaultVariants = resolved.defaultVariants;
  component.compoundSlots = resolved.compoundSlots;
  component.compoundVariants = resolved.compoundVariants;
};
var getTailwindVariants = (cn) => {
  const tv = (options, configProp) => {
    const resolved = resolveOptions(options, configProp);
    const component = createClassResolver(resolved, cn);
    attachComponentMetadata(component, resolved);
    return component;
  };
  const createTV = (configProp) => {
    return (options, config) => tv(options, config ? chunk2BFDQGZN_cjs.mergeObjects(configProp, config) : configProp);
  };
  return {
    tv,
    createTV
  };
};

exports.defaultConfig = defaultConfig;
exports.getTailwindVariants = getTailwindVariants;
exports.state = state;
