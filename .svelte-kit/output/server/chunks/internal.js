//#region node_modules/@sveltejs/kit/src/runtime/app/paths/internal/server.js
var base = "";
var assets = base;
var app_dir = "_app";
var initial = {
	base,
	assets
};
/**
* `base` could be overridden during rendering to be relative;
* this one's the original non-relative base path
*/
var initial_base = initial.base;
/**
* @param {{ base: string, assets: string }} paths
*/
function override(paths) {
	base = paths.base;
	assets = paths.assets;
}
function reset() {
	base = initial.base;
	assets = initial.assets;
}
/** @param {string} path */
function set_assets(path) {
	assets = initial.assets = path;
}
var prerendering = false;
function set_building() {}
function set_prerendering() {
	prerendering = true;
}
//#endregion
export { assets as a, override as c, app_dir as i, reset as l, set_building as n, base as o, set_prerendering as r, initial_base as s, prerendering as t, set_assets as u };
