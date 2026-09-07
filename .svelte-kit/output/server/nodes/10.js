

export const index = 10;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/terms/_page.svelte.js')).default;
export const imports = ["_app/immutable/nodes/10.C74ogMxl.js","_app/immutable/chunks/CtRreaCv.js","_app/immutable/chunks/xihTtKlq.js"];
export const stylesheets = [];
export const fonts = [];
