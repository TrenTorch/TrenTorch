"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.FunctionRegion = exports.FunctionsHttpError = exports.FunctionsRelayError = exports.FunctionsFetchError = exports.FunctionsError = void 0;
/**
 * Base error for Supabase Edge Function invocations.
 *
 * @example
 * ```ts
 * import { FunctionsError } from '@supabase/functions-js'
 *
 * throw new FunctionsError('Unexpected error invoking function', 'FunctionsError', {
 *   requestId: 'abc123',
 * })
 * ```
 */
class FunctionsError extends Error {
    constructor(message, name = 'FunctionsError', context) {
        super(message);
        this.name = name;
        this.context = context;
    }
    toJSON() {
        return {
            name: this.name,
            message: this.message,
            context: this.context,
        };
    }
}
exports.FunctionsError = FunctionsError;
/**
 * Error thrown when the network request to an Edge Function fails.
 *
 * @example
 * ```ts
 * import { FunctionsFetchError } from '@supabase/functions-js'
 *
 * throw new FunctionsFetchError({ requestId: 'abc123' })
 * ```
 */
class FunctionsFetchError extends FunctionsError {
    constructor(context) {
        super('Failed to send a request to the Edge Function', 'FunctionsFetchError', context);
    }
}
exports.FunctionsFetchError = FunctionsFetchError;
/**
 * Error thrown when the Supabase relay cannot reach the Edge Function.
 *
 * @example
 * ```ts
 * import { FunctionsRelayError } from '@supabase/functions-js'
 *
 * throw new FunctionsRelayError({ region: 'us-east-1' })
 * ```
 */
class FunctionsRelayError extends FunctionsError {
    constructor(context) {
        super('Relay Error invoking the Edge Function', 'FunctionsRelayError', context);
    }
}
exports.FunctionsRelayError = FunctionsRelayError;
/**
 * Error thrown when the Edge Function returns a non-2xx status code.
 *
 * @example
 * ```ts
 * import { FunctionsHttpError } from '@supabase/functions-js'
 *
 * throw new FunctionsHttpError({ status: 500 })
 * ```
 */
class FunctionsHttpError extends FunctionsError {
    constructor(context) {
        super('Edge Function returned a non-2xx status code', 'FunctionsHttpError', context);
    }
}
exports.FunctionsHttpError = FunctionsHttpError;
// Define the enum for the 'region' property
var FunctionRegion;
(function (FunctionRegion) {
    FunctionRegion["Any"] = "any";
    FunctionRegion["ApNortheast1"] = "ap-northeast-1";
    FunctionRegion["ApNortheast2"] = "ap-northeast-2";
    FunctionRegion["ApSouth1"] = "ap-south-1";
    FunctionRegion["ApSoutheast1"] = "ap-southeast-1";
    FunctionRegion["ApSoutheast2"] = "ap-southeast-2";
    FunctionRegion["CaCentral1"] = "ca-central-1";
    FunctionRegion["EuCentral1"] = "eu-central-1";
    FunctionRegion["EuWest1"] = "eu-west-1";
    FunctionRegion["EuWest2"] = "eu-west-2";
    FunctionRegion["EuWest3"] = "eu-west-3";
    FunctionRegion["SaEast1"] = "sa-east-1";
    FunctionRegion["UsEast1"] = "us-east-1";
    FunctionRegion["UsWest1"] = "us-west-1";
    FunctionRegion["UsWest2"] = "us-west-2";
})(FunctionRegion || (exports.FunctionRegion = FunctionRegion = {}));
//# sourceMappingURL=types.js.map