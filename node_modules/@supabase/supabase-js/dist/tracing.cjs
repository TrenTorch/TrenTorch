const require_tracingRegistry = require('./tracingRegistry.cjs');
let _opentelemetry_api = require("@opentelemetry/api");

//#region ../../shared/tracing/dist/module/create-extractor.js
/**
* Build a {@link TraceContextExtractor} from an OpenTelemetry API object.
*
* The extractor injects the active context into a fresh carrier on every
* call and returns the W3C trace headers found there. When there is no
* `traceparent`, it returns null for an empty carrier (no active trace) or
* a headerless result carrying only {@link TraceExtractionResult.carrierKeys}
* when the propagator wrote non-W3C headers. Returns null when the API
* throws.
*/
function createTraceContextExtractor(otel) {
	return () => {
		try {
			const carrier = {};
			otel.propagation.inject(otel.context.active(), carrier);
			const traceparent = carrier["traceparent"];
			if (!traceparent) {
				const carrierKeys = Object.keys(carrier);
				if (carrierKeys.length === 0) return null;
				return { carrierKeys };
			}
			return {
				traceparent,
				tracestate: carrier["tracestate"],
				baggage: carrier["baggage"]
			};
		} catch (_a) {
			return null;
		}
	};
}

//#endregion
//#region src/tracing.ts
/**
* Opt-in OpenTelemetry runtime for `tracePropagation`.
*
* Importing this module registers the OpenTelemetry trace context extractor
* used by every Supabase client in the process. It has no exports — the
* import itself is the opt-in:
*
* ```ts
* import '@supabase/supabase-js/tracing'
* import { createClient } from '@supabase/supabase-js'
*
* const supabase = createClient(url, key, { tracePropagation: true })
* ```
*
* Requires `@opentelemetry/api` to be installed — this module imports it
* directly, so bundlers include it and resolution fails loudly when it is
* missing. Without this import, enabling `tracePropagation` logs a one-time
* warning and requests are sent without trace headers.
*
* @module tracing
*/
require_tracingRegistry.registerTraceContextExtractor(createTraceContextExtractor({
	propagation: _opentelemetry_api.propagation,
	context: _opentelemetry_api.context
}));

//#endregion
//# sourceMappingURL=tracing.cjs.map