import fs from "fs";
import path from "path";
import { createRequire } from "module";
import { normalizeParserOptions } from "./parser/parser-options.js";
import { svelteToVirtualTypeScript } from "./parser/svelte-to-virtual-ts.js";
import { loadNewestModule } from "./utils/cjs-module.js";
/**
 * Experimental hook that intercepts `ts.sys.readFile` and returns virtual
 * TypeScript for `.svelte` paths. ESLint's own reads go through `fs` and
 * are unaffected. Activate with `SVELTE_ESLINT_PARSER_EXPERIMENTAL_TS_SYS_HOOK=1`.
 *
 * Several preconditions must hold for the hook to actually speed anything up
 * (extraFileExtensions includes '.svelte', type-aware lint is on, the TS
 * instance is reachable through CJS require.cache). When the hook is opted
 * in but a precondition fails, a warning is emitted so users can diagnose
 * why no speed-up materialised.
 */
const ENV_FLAG = "SVELTE_ESLINT_PARSER_EXPERIMENTAL_TS_SYS_HOOK";
const translations = new Map();
const patchedSysObjects = new WeakSet();
let activeParserOptions = null;
let fallbackParserOptions = undefined;
let installed = false;
let needsParseTimeRescan = false;
let parserOptionsInspected = false;
let patchAppliedCount = 0;
let primeStoredCount = 0;
let svelteReadFileCount = 0;
function warn(msg) {
    process.stderr.write(`[svelte-eslint-parser:ts-sys-hook] WARNING: ${msg}\n`);
}
/** Called from `parseForESLint` so translation has the user's parser config. */
export function rememberParserOptions(options) {
    const hadOptions = activeParserOptions !== null;
    activeParserOptions = options;
    // Drop fallback translations so they are redone with the real options.
    if (!hadOptions) {
        for (const [filePath, entry] of translations) {
            if (entry.provisional)
                translations.delete(filePath);
        }
    }
    if (installed && !parserOptionsInspected) {
        parserOptionsInspected = true;
        inspectParserOptions(options);
    }
    // Catch a TypeScript instance that landed in `require.cache` between
    // `installTsSysHook` and the first parse (e.g. typescript-eslint loaded
    // after svelte-eslint-parser in `eslint.config.js`). Walking on every
    // subsequent parse would be wasteful and gains nothing — TS instances
    // are not added back later in a typical lint run.
    if (!needsParseTimeRescan)
        return;
    needsParseTimeRescan = false;
    patchAllLoadedTypeScripts();
}
function inspectParserOptions(options) {
    // `extraFileExtensions` lives on the raw options object; normalize spreads
    // it through, even though it isn't part of the typed interface.
    const raw = options;
    const extra = raw.extraFileExtensions;
    const hasSvelteExt = Array.isArray(extra) && extra.includes(".svelte");
    if (!hasSvelteExt) {
        warn("parserOptions.extraFileExtensions does not include '.svelte'. " +
            "ts.sys.readFile will not be called for .svelte paths, so the hook " +
            "cannot speed anything up.");
    }
    if (options.project == null &&
        options.projectService == null &&
        options.EXPERIMENTAL_useProjectService == null) {
        warn("neither `project` nor `projectService` is configured. The hook only " +
            "helps when typescript-eslint is doing type-aware lint.");
    }
}
/** Seed the cache so a later `ts.sys.readFile` skips re-translating. */
export function primeTranslationCache(filePath, virtualCode) {
    if (!installed)
        return;
    // Skip the stat + write if on-demand translation already cached a positive
    // entry — the prime is redundant when ts.sys read the file before ESLint did.
    const existing = translations.get(filePath);
    if (existing && existing.virtualCode !== null && !existing.provisional) {
        return;
    }
    const mtimeMs = statMtimeMs(filePath);
    if (mtimeMs === null)
        return;
    translations.set(filePath, { mtimeMs, virtualCode, provisional: false });
    primeStoredCount++;
}
function statMtimeMs(filePath) {
    try {
        return fs.statSync(filePath).mtimeMs;
    }
    catch {
        return null;
    }
}
function readUtf8(filePath) {
    try {
        return fs.readFileSync(filePath, "utf-8");
    }
    catch {
        return null;
    }
}
/** Fallback options for translations requested before the first `.svelte` parse. */
function getFallbackParserOptions() {
    if (fallbackParserOptions !== undefined)
        return fallbackParserOptions;
    try {
        fallbackParserOptions = normalizeParserOptions({
            parser: loadNewestModule("@typescript-eslint/parser"),
        });
    }
    catch {
        fallbackParserOptions = null;
    }
    return fallbackParserOptions;
}
function translateOnDemand(filePath) {
    const parserOptions = activeParserOptions ?? getFallbackParserOptions();
    if (!parserOptions)
        return null;
    const provisional = activeParserOptions === null;
    const mtimeMs = statMtimeMs(filePath);
    if (mtimeMs === null)
        return null;
    const cached = translations.get(filePath);
    if (cached && cached.mtimeMs === mtimeMs)
        return cached.virtualCode;
    const svelteSource = readUtf8(filePath);
    if (svelteSource === null) {
        translations.set(filePath, { mtimeMs, virtualCode: null, provisional });
        return null;
    }
    const virtualCode = svelteToVirtualTypeScript(filePath, svelteSource, parserOptions);
    // Store the outcome — including `null` — to negative-cache failed translations.
    translations.set(filePath, { mtimeMs, virtualCode, provisional });
    return virtualCode;
}
function patchTsSys(sys) {
    if (!sys || typeof sys.readFile !== "function")
        return;
    if (patchedSysObjects.has(sys))
        return;
    patchedSysObjects.add(sys);
    patchAppliedCount++;
    const originalReadFile = sys.readFile.bind(sys);
    sys.readFile = (filePath, encoding) => {
        if (typeof filePath === "string" && filePath.endsWith(".svelte")) {
            svelteReadFileCount++;
            const virtual = translateOnDemand(filePath);
            if (virtual !== null)
                return virtual;
        }
        return originalReadFile(filePath, encoding);
    };
}
/**
 * Force-load the project's TypeScript so it lands in `require.cache`. The
 * patch then happens through `patchAllLoadedTypeScripts`; no need to capture
 * the returned module ourselves.
 */
function ensureTypeScriptLoaded() {
    try {
        loadNewestModule("typescript");
    }
    catch (e) {
        warn(`failed to load 'typescript' from the project: ${e instanceof Error ? e.message : String(e)}. The hook has nothing to patch.`);
    }
}
/** Patch every `typescript.js` already in `require.cache`. */
function patchAllLoadedTypeScripts() {
    const cache = createRequire(import.meta.url).cache;
    if (!cache)
        return;
    for (const [resolvedPath, mod] of Object.entries(cache)) {
        if (resolvedPath.includes(`${path.sep}typescript${path.sep}`) &&
            resolvedPath.endsWith(`${path.sep}typescript.js`)) {
            patchTsSys(mod?.exports?.sys);
        }
    }
}
/** Idempotent. No-op unless `SVELTE_ESLINT_PARSER_EXPERIMENTAL_TS_SYS_HOOK=1`. */
export function installTsSysHook() {
    if (installed)
        return;
    // eslint-disable-next-line no-process-env -- intentional opt-in gate
    if (process.env[ENV_FLAG] !== "1")
        return;
    ensureTypeScriptLoaded();
    patchAllLoadedTypeScripts();
    installed = true;
    // Arm a one-shot rescan; see `rememberParserOptions`.
    needsParseTimeRescan = true;
    // End-of-run check: if .svelte files were linted but the patched readFile
    // was never hit for any of them, the hook silently did nothing.
    process.on("exit", () => {
        if (primeStoredCount > 0 && svelteReadFileCount === 0) {
            warn("ts.sys.readFile was never called for a .svelte path even though " +
                `${primeStoredCount} .svelte file(s) were parsed. Likely causes: ` +
                "parserOptions.extraFileExtensions missing '.svelte', " +
                "typescript-eslint not running type-aware lint, " +
                "or the TS instance it uses was not in CJS require.cache " +
                "(e.g. ESM-loaded).");
        }
        else if (patchAppliedCount === 0) {
            warn("no `typescript.js` was found in CJS require.cache, so nothing was " +
                "patched. The TS instance used by typescript-eslint may be " +
                "ESM-loaded or otherwise outside the cache.");
        }
    });
    // Visible on every lint run so users know they opted into an experiment.
    process.stderr.write(`[svelte-eslint-parser] ${ENV_FLAG}=1 enables an experimental ts.sys.readFile hook. ` +
        `Behavior and API may change or be removed in any release.\n`);
}
/** Test seam. The `ts.sys` patches themselves are intentionally permanent. */
export function _resetTranslationCacheForTesting() {
    translations.clear();
    activeParserOptions = null;
    fallbackParserOptions = undefined;
    needsParseTimeRescan = false;
}
/** Test seam: patch a caller-supplied `sys` instead of the require.cache ones. */
export function _patchTsSysForTesting(sys) {
    patchTsSys(sys);
}
