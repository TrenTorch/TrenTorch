import * as universal from '../entries/pages/_page.ts.js';

export const index = 2;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_page.svelte.js')).default;
export { universal };
export const universal_id = "platform/routes/+page.ts";
export const imports = ["_app/immutable/nodes/2.BOmkUGzy.js","_app/immutable/chunks/CtRreaCv.js","_app/immutable/chunks/gcVDSUzf.js","_app/immutable/chunks/xihTtKlq.js","_app/immutable/chunks/C2P02Z9O.js","_app/immutable/chunks/B61uhBPF.js","_app/immutable/chunks/CMj8s_eX.js","_app/immutable/chunks/Ccf55TNZ.js","_app/immutable/chunks/DRLdq8YX.js","_app/immutable/chunks/Bg_HSZ0I.js","_app/immutable/chunks/CmE6OttZ.js"];
export const stylesheets = ["_app/immutable/assets/2.BZw7ZzQF.css"];
export const fonts = [];
