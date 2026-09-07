import { CnOptions, CnReturn } from './types.js';
import './config-bO3A8WhU.js';

declare const removeExtraSpaces: (str: string) => string;
declare const cx: <T extends CnOptions>(...classnames: T) => CnReturn;
declare const falsyToString: <T>(value: T) => T | string;
declare const isEmptyObject: (obj: unknown) => boolean;
declare const isEqual: (obj1: object, obj2: object) => boolean;
declare const isBoolean: (value: unknown) => boolean;
declare const joinObjects: <T extends Record<string, unknown>, U extends Record<string, unknown>>(obj1: T, obj2: U) => T & U;
declare const flat: <T>(arr: unknown[], target: T[]) => void;
declare function flatArray<T>(arr: unknown[]): T[];
declare const flatMergeArrays: <T>(...arrays: unknown[][]) => T[];
declare const mergeObjects: <T extends object, U extends object>(obj1: T, obj2: U) => Record<string, unknown>;

export { cx, falsyToString, flat, flatArray, flatMergeArrays, isBoolean, isEmptyObject, isEqual, joinObjects, mergeObjects, removeExtraSpaces };
