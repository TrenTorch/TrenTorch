import { CnOptions, CnReturn, TVLite } from './types.cjs';
export { ClassProp, OmitUndefined, StringToBoolean, TV, TVCompoundSlots, TVCompoundVariants, TVDefaultVariants, TVProps, TVReturnProps, TVReturnType, TVReturnTypeLike, TVScreenPropsValue, TVVariantKeys, TVVariants, VariantProps, WithInitialScreen, isTrueOrArray } from './types.cjs';
export { cx } from './utils.cjs';
export { C as ClassValue } from './config-bO3A8WhU.cjs';

declare const cn: <T extends CnOptions>(...classnames: T) => ((config?: any) => CnReturn);
declare const tv: TVLite;
declare const createTV: () => TVLite;

export { CnOptions, CnReturn, TVLite, cn, createTV, tv };
