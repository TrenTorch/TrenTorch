import type { TSESTree } from "@typescript-eslint/types";
import type ESTree from "estree";
/**
 * Add element to a sorted array
 */
export declare function addElementToSortedArray<T>(array: T[], element: T, compare: (a: T, b: T) => number): void;
/**
 * Add element to a sorted array
 */
export declare function addElementsToSortedArray<T>(array: T[], elements: T[], compare: (a: T, b: T) => number): void;
/**
 * Uses a binary search to determine the highest index at which value should be inserted into array in order to maintain its sort order.
 */
export declare function sortedLastIndex<T>(array: T[], compare: (target: T) => number): number;
/**
 * Checks if the given element has type information.
 *
 * Note: This function is not exhaustive and does not cover all possible cases.
 * However, it works sufficiently well for this parser.
 * @param element The element to check.
 * @returns True if the element has type information, false otherwise.
 */
export declare function hasTypeInfo(element: ESTree.Expression | TSESTree.Expression): boolean;
