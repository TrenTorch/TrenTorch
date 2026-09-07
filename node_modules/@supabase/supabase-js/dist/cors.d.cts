//#region src/cors.d.ts
/**
 * Canonical CORS configuration for Supabase Edge Functions
 *
 * This module exports CORS headers kept in sync with the headers the Supabase
 * SDK sends. Using it in Edge Functions prevents CORS preflight errors when the
 * SDK adds new headers — update SUPABASE_HEADERS whenever the SDK starts
 * sending one (enforced by the unit tests).
 *
 * @example Basic usage
 * ```typescript
 * import { corsHeaders } from '@supabase/supabase-js/cors'
 *
 * Deno.serve(async (req) => {
 *   if (req.method === 'OPTIONS') {
 *     return new Response('ok', { headers: corsHeaders })
 *   }
 *
 *   return new Response(
 *     JSON.stringify({ data: 'Hello' }),
 *     { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
 *   )
 * })
 * ```
 *
 * @module cors
 */
/**
 * Type representing CORS headers as a record of header names to values
 */
type CorsHeaders = Record<string, string>;
/**
 * Default CORS headers for Supabase Edge Functions.
 *
 * Includes all headers sent by Supabase client libraries and allows all standard HTTP methods.
 * Use this for simple CORS configurations with wildcard origin.
 *
 * @example Basic usage
 * ```typescript
 * import { corsHeaders } from '@supabase/supabase-js/cors'
 *
 * Deno.serve(async (req) => {
 *   if (req.method === 'OPTIONS') {
 *     return new Response('ok', { headers: corsHeaders })
 *   }
 *
 *   return new Response(
 *     JSON.stringify({ data: 'Hello' }),
 *     { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
 *   )
 * })
 * ```
 *
 * @category Edge Functions
 */
declare const corsHeaders: CorsHeaders;
//#endregion
export { CorsHeaders, corsHeaders };
//# sourceMappingURL=cors.d.cts.map