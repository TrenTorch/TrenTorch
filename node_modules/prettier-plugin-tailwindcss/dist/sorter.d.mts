//#region src/sorter.d.ts
interface SorterOptions {
  /**
   * The directory used to resolve relative file paths.
   *
   * When not provided this will be:
   * - The current working directory
   */
  base?: string;
  /**
   * The path to the file being formatted.
   *
   * When provided, Tailwind CSS is resolved relative to this path; otherwise,
   * it is resolved relative to `base`.
   */
  filepath?: string;
  /**
   * Path to the Tailwind CSS config file (v3).
   *
   * Paths are resolved relative to `base`.
   */
  configPath?: string;
  /**
   * Path to the CSS stylesheet used by Tailwind CSS (v4+).
   *
   * Paths are resolved relative to `base`.
   */
  stylesheetPath?: string;
  /**
   * Whether or not to preserve whitespace around classes.
   *
   * Default: false
   */
  preserveWhitespace?: boolean;
  /**
   * Whether or not to preserve duplicate classes.
   *
   * Default: false
   */
  preserveDuplicates?: boolean;
}
interface Sorter {
  /**
   * Sort one or more class attributes.
   *
   * Each element is the value of an HTML `class` attribute (or similar). i.e. a
   * space separated list of class names as a string.
   */
  sortClassAttributes(classes: string[]): string[];
  /**
   * Sort one or more class lists.
   *
   * Each element is an array of class names. Passing a space separated class
   * list in each element is not supported.
   *
   * Duplicates are removed by default unless `preserveDuplicates` is enabled.
   */
  sortClassLists(classes: string[][]): string[][];
}
/**
 * Creates a sorter instance for sorting Tailwind CSS classes.
 *
 * This function initializes a sorter with the specified Tailwind CSS configuration.
 * The sorter can be used to sort class attributes (space-separated strings) or
 * class lists (arrays of class names).

 * @example
 * ```ts
 * const sorter = await createSorter({})
 *
 * // Sort class lists
 * const sorted = sorter.sortClassLists([['p-4', 'm-2']])
 * // Returns: [['m-2', 'p-4']]
 * ```
 */
declare function createSorter(opts: SorterOptions): Promise<Sorter>;
//#endregion
export { Sorter, SorterOptions, createSorter };