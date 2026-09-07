import path from "node:path";
import { lte } from "semver";
import { createRequire } from "node:module";
const cachedRequires = {};
/** Load the newest reachable copy of a module (linter → cwd → self). */
export function loadNewestModule(module) {
    const requires = [
        getRequireFromLinter(),
        getRequireFromCwd(),
        createRequire(import.meta.url),
    ];
    const versionAndGetterList = [];
    for (const require of requires) {
        if (!require)
            continue;
        try {
            const pkg = require(`${module}/package.json`);
            versionAndGetterList.push({ version: pkg.version, require });
        }
        catch {
            // ignore
        }
    }
    // Sort by version, newest first
    versionAndGetterList.sort((a, b) => (lte(a.version, b.version) ? 1 : -1));
    let error = null;
    for (const { require } of versionAndGetterList) {
        try {
            return require(module);
        }
        catch (e) {
            error ?? (error = e instanceof Error ? e : new Error(String(e)));
        }
    }
    throw error ?? new Error(`Cannot find module '${module}'`);
}
/**
 * Get NodeJS.Require from Linter
 */
function getRequireFromLinter() {
    if (cachedRequires.fromLinter)
        return cachedRequires.fromLinter;
    try {
        const req = createRequire(import.meta.url);
        const linterPathFromRequire = Object.keys(req.cache || {}).find(isLinterPath);
        if (linterPathFromRequire) {
            try {
                cachedRequires.fromLinter = createRequire(linterPathFromRequire);
            }
            catch {
                // ignore
            }
        }
    }
    catch {
        // ignore
    }
    try {
        const eslintPkgPath = getRequireFromCwd()?.resolve("eslint/package.json");
        if (!eslintPkgPath)
            return null;
        const relativeTo = path.join(path.dirname(eslintPkgPath), "__placeholder__.js");
        return (cachedRequires.fromLinter = createRequire(relativeTo));
    }
    catch {
        // ignore
    }
    return null;
}
/**
 * Get NodeJS.Require from Cwd
 */
function getRequireFromCwd() {
    if (cachedRequires.fromCwd)
        return cachedRequires.fromCwd;
    try {
        const cwd = process.cwd();
        const relativeTo = path.join(cwd, "__placeholder__.js");
        return (cachedRequires.fromCwd = createRequire(relativeTo));
    }
    catch {
        // ignore
    }
    return null;
}
/** Checks if given path is linter path */
function isLinterPath(p) {
    return (
    // ESLint 6 and above
    p.includes(`eslint${path.sep}lib${path.sep}linter${path.sep}linter.js`) ||
        // ESLint 5
        p.includes(`eslint${path.sep}lib${path.sep}linter.js`));
}
