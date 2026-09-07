import * as prettier0 from "prettier";
import { SupportOption } from "prettier";

//#region src/options.d.ts
declare const options: Record<string, SupportOption>;
//#endregion
//#region src/index.d.ts
declare const parsers: Record<string, prettier0.Parser<any> | (() => Promise<prettier0.Parser<any> | undefined>) | undefined>, printers: Record<string, prettier0.Printer<any> | (() => Promise<prettier0.Printer<any> | undefined>) | undefined>;
interface PluginOptions {
  /**
   * Path to the Tailwind config file.
   */
  tailwindConfig?: string;
  /**
   * Path to the CSS stylesheet used by Tailwind CSS (v4+)
   */
  tailwindStylesheet?: string;
  /**
   * Path to the CSS stylesheet used by Tailwind CSS (v4+)
   *
   * @deprecated Use `tailwindStylesheet` instead
   */
  tailwindEntryPoint?: string;
  /**
   * List of custom function and tag names that contain classes.
   *
   * Default: []
   */
  tailwindFunctions?: string[];
  /**
   * List of custom attributes that contain classes.
   *
   * Default: []
   */
  tailwindAttributes?: string[];
  /**
   * Preserve whitespace around Tailwind classes when sorting.
   *
   * Default: false
   */
  tailwindPreserveWhitespace?: boolean;
  /**
   * Preserve duplicate classes inside a class list when sorting.
   *
   * Default: false
   */
  tailwindPreserveDuplicates?: boolean;
}
//#endregion
export { PluginOptions, options, parsers, printers };