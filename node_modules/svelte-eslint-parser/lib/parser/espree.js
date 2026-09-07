import { loadNewestModule } from "../utils/cjs-module.js";
import * as espree from "espree";
let espreeCache = null;
/**
 * Load `espree` from ESLint's dependencies, user dependencies, or this package's dependencies.
 * Return the latest version among them.
 */
export function getEspree() {
    if (!espreeCache) {
        try {
            espreeCache = loadNewestModule("espree");
        }
        catch {
            // ignore
        }
        if (!espreeCache) {
            espreeCache = espree.default || espree;
        }
    }
    return espreeCache;
}
