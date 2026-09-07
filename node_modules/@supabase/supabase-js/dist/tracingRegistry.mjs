//#region src/lib/tracingRegistry.ts
const EXTRACTOR_KEY = Symbol.for("@supabase/supabase-js.traceContextExtractor");
/**
* Register the trace context extractor used by all Supabase clients in this
* process. Called by the `@supabase/supabase-js/tracing` subpath as an import
* side effect; the last registration wins.
*/
function registerTraceContextExtractor(extractor) {
	globalThis[EXTRACTOR_KEY] = extractor;
}
/**
* The currently registered trace context extractor, if any.
*/
function getTraceContextExtractor() {
	return globalThis[EXTRACTOR_KEY];
}

//#endregion
export { registerTraceContextExtractor as n, getTraceContextExtractor as t };
//# sourceMappingURL=tracingRegistry.mjs.map