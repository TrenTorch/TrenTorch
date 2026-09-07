import { CnOptions, CnReturn, TV } from './types.js';
export { ClassProp, OmitUndefined, StringToBoolean, TVCompoundSlots, TVCompoundVariants, TVDefaultVariants, TVLite, TVProps, TVReturnProps, TVReturnType, TVReturnTypeLike, TVScreenPropsValue, TVVariantKeys, TVVariants, VariantProps, WithInitialScreen, isTrueOrArray } from './types.js';
import { T as TWMConfig, a as TVConfig } from './config-bO3A8WhU.js';
export { C as ClassValue, b as TWMergeConfig } from './config-bO3A8WhU.js';

/**
 * Combines class names and merges conflicting Tailwind classes (default config).
 */
declare const cn: <T extends CnOptions>(...classnames: T) => CnReturn;
/**
 * Combines class names and merges conflicting Tailwind classes.
 * Pass optional `twMerge` / `twMergeConfig` on the second call.
 */
declare const cnMerge: <T extends CnOptions>(...classnames: T) => ((config?: TWMConfig) => CnReturn);

/**
 * Creates a variant-aware component function with Tailwind CSS classes.
 * Supports variants, slots, compound variants, and component composition.
 * @see https://www.tailwind-variants.org/docs/getting-started
 */
declare const tv: TV;
/**
 * Creates a configured `tv` instance with custom default configuration.
 */
declare const createTV: (config: TVConfig) => TV;
/**
 * Default configuration object for tailwind-variants.
 */
declare const defaultConfig: TVConfig;
/**
 * Combines class names without merging conflicting Tailwind CSS classes.
 */
declare const cx: <T extends CnOptions>(...classnames: T) => CnReturn;

export { CnOptions, CnReturn, TV, TVConfig, TWMConfig, cn, cnMerge, createTV, cx, defaultConfig, tv };
