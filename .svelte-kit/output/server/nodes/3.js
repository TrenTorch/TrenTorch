import * as universal from '../entries/pages/account/_page.ts.js';

export const index = 3;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/account/_page.svelte.js')).default;
export { universal };
export const universal_id = "platform/routes/account/+page.ts";
export const imports = ["_app/immutable/nodes/3.D5obCy5u.js","_app/immutable/chunks/CtRreaCv.js","_app/immutable/chunks/gcVDSUzf.js","_app/immutable/chunks/xihTtKlq.js","_app/immutable/chunks/C3MuKl3W.js","_app/immutable/chunks/CMj8s_eX.js","_app/immutable/chunks/DusSgSBD.js","_app/immutable/chunks/CfqD3z1W.js","_app/immutable/chunks/CVNPiL0N.js","_app/immutable/chunks/DRLdq8YX.js","_app/immutable/chunks/DaZ64DTv.js","_app/immutable/chunks/Bg_HSZ0I.js","_app/immutable/chunks/CmE6OttZ.js","_app/immutable/chunks/BrMgeoLE.js","_app/immutable/chunks/DnfNWNiv.js"];
export const stylesheets = [];
export const fonts = [];
