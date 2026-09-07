import { CnOptions, CnReturn, TVLite } from './types.js';
export { ClassProp, OmitUndefined, StringToBoolean, TV, TVCompoundSlots, TVCompoundVariants, TVDefaultVariants, TVProps, TVReturnProps, TVReturnType, TVReturnTypeLike, TVScreenPropsValue, TVVariantKeys, TVVariants, VariantProps, WithInitialScreen, isTrueOrArray } from './types.js';
export { cx } from './utils.js';
export { C as ClassValue } from './config-bO3A8WhU.js';

declare const cn: <T extends CnOptions>(...classnames: T) => ((config?: any) => CnReturn);
declare const tv: TVLite;
declare const createTV: () => TVLite;

export { CnOptions, CnReturn, TVLite, cn, createTV, tv };
