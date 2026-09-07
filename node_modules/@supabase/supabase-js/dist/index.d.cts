import { FunctionInvokeOptions, FunctionRegion, FunctionsClient, FunctionsError, FunctionsFetchError, FunctionsHttpError, FunctionsRelayError } from "@supabase/functions-js";
import { PostgrestBuilder, PostgrestClient, PostgrestError, PostgrestError as PostgrestError$1, PostgrestFilterBuilder, PostgrestFilterBuilder as PostgrestFilterBuilder$1, PostgrestMaybeSingleResponse, PostgrestOpenApiSpec, PostgrestOpenApiSpec as PostgrestOpenApiSpec$1, PostgrestQueryBuilder, PostgrestQueryBuilder as PostgrestQueryBuilder$1, PostgrestResponse, PostgrestSingleResponse, PostgrestSingleResponse as PostgrestSingleResponse$1, PostgrestTransformBuilder } from "@supabase/postgrest-js";
import { RealtimeChannel, RealtimeChannelOptions, RealtimeClient, RealtimeClientOptions, RealtimeRemoveChannelResponse } from "@supabase/realtime-js";
import { StorageApiError, StorageClient, StorageClientOptions } from "@supabase/storage-js";
import { AuthClient, GoTrueClientOptions, Session as AuthSession, User as AuthUser } from "@supabase/auth-js";
export * from "@supabase/realtime-js";
export * from "@supabase/auth-js";

//#region src/lib/rest/types/common/common.d.ts

type GenericRelationship = {
  foreignKeyName: string;
  columns: string[];
  isOneToOne?: boolean;
  referencedRelation: string;
  referencedColumns: string[];
};
type GenericTable = {
  Row: Record<string, unknown>;
  Insert: Record<string, unknown>;
  Update: Record<string, unknown>;
  Relationships: GenericRelationship[];
};
type GenericUpdatableView = {
  Row: Record<string, unknown>;
  Insert: Record<string, unknown>;
  Update: Record<string, unknown>;
  Relationships: GenericRelationship[];
};
type GenericNonUpdatableView = {
  Row: Record<string, unknown>;
  Relationships: GenericRelationship[];
};
type GenericView = GenericUpdatableView | GenericNonUpdatableView;
type GenericSetofOption = {
  isSetofReturn?: boolean | undefined;
  isOneToOne?: boolean | undefined;
  isNotNullable?: boolean | undefined;
  to: string;
  from: string;
};
type GenericFunction = {
  Args: Record<string, unknown> | never;
  Returns: unknown;
  SetofOptions?: GenericSetofOption;
};
type GenericSchema = {
  Tables: Record<string, GenericTable>;
  Views: Record<string, GenericView>;
  Functions: Record<string, GenericFunction>;
};
//#endregion
//#region src/lib/types.d.ts
interface SupabaseAuthClientOptions extends GoTrueClientOptions {}
type Fetch = typeof fetch;
/**
 * Configuration options for trace context propagation.
 *
 * Enables distributed tracing across Supabase services using W3C Trace Context
 * and OpenTelemetry standards. When enabled, the SDK automatically attaches
 * trace context headers (`traceparent`, `tracestate`, `baggage`) to outgoing
 * requests to Supabase domains. The resulting `trace_id` appears in API
 * Gateway and Edge Function logs, so logs forwarded through Log Drains can
 * be correlated back to the originating client-side span.
 *
 * Requires two opt-in steps: install `@opentelemetry/api` in the consuming
 * application, and load the tracing runtime with
 * `import '@supabase/supabase-js/tracing'` at the application entry point.
 * If the runtime is not loaded, the SDK logs a one-time warning and sends
 * requests without trace headers; if there is no active context at request
 * time, propagation silently no-ops. Not available via the CDN/UMD build.
 *
 * @example Enable with defaults
 * ```ts
 * import '@supabase/supabase-js/tracing'
 *
 * const supabase = createClient(url, key, {
 *   tracePropagation: { enabled: true },
 * })
 * ```
 *
 * @see https://www.w3.org/TR/trace-context/
 * @see https://opentelemetry.io/docs/concepts/context-propagation/
 * @see https://supabase.com/docs/guides/telemetry/client-side-tracing
 */
interface TracePropagationOptions {
  /**
   * Enable trace propagation. Disabled by default.
   *
   * When enabled, automatically detects and propagates active trace context
   * from the OpenTelemetry API to outgoing Supabase requests. Trace context
   * is only propagated to Supabase domains (`*.supabase.co`, `*.supabase.in`,
   * `localhost`) for security — third-party hosts never receive trace headers.
   *
   * @default false
   *
   * @example
   * ```ts
   * import '@supabase/supabase-js/tracing'
   *
   * const supabase = createClient(url, key, {
   *   tracePropagation: { enabled: true },
   * })
   * ```
   */
  enabled?: boolean;
  /**
   * Respect upstream sampling decisions.
   *
   * When true (the default), requests whose upstream trace is not sampled
   * (sampled flag = `0` in the `traceparent` header) carry only the
   * `traceparent` header — the sampled flag is preserved, so downstream
   * tracing never records them, while Supabase logs still get a `trace_id`
   * to correlate on. The `tracestate` and `baggage` headers are withheld on
   * these requests.
   *
   * Set to `false` to always propagate the full trace context
   * (`traceparent`, `tracestate`, `baggage`) regardless of the sampling
   * decision.
   *
   * @default true
   *
   * @example Always propagate the full context, ignore sampling
   * ```ts
   * import '@supabase/supabase-js/tracing'
   *
   * const supabase = createClient(url, key, {
   *   tracePropagation: { enabled: true, respectSamplingDecision: false },
   * })
   * ```
   */
  respectSamplingDecision?: boolean;
}
type SupabaseClientOptions<SchemaName> = {
  /**
   * The Postgres schema which your tables belong to. Must be on the list of exposed schemas in Supabase. Defaults to `public`.
   *
   * With generated `Database` types, this type-checks against schemas other than `public` only when the schema name is also passed as the second generic to `createClient`, e.g. `createClient<Database, 'myschema'>(url, key, { db: { schema: 'myschema' } })`. `supabase.schema('myschema').from(...)` infers its schema per call and needs no second generic.
   */
  db?: {
    schema?: SchemaName;
    /**
     * Optional timeout in milliseconds for PostgREST requests.
     * When set, requests will automatically abort after this duration to prevent indefinite hangs.
     *
     * @example With timeout
     * ```ts
     * const supabase = createClient(url, key, {
     *   db: { timeout: 30000 } // 30 second timeout
     * })
     * ```
     */
    timeout?: number;
    /**
     * Maximum URL length in characters before warnings/errors are triggered.
     * Defaults to 8000 characters. Used to provide helpful hints when URLs
     * exceed server limits.
     *
     * @example With custom URL length limit
     * ```ts
     * const supabase = createClient(url, key, {
     *   db: { urlLengthLimit: 10000 } // Custom limit
     * })
     * ```
     */
    urlLengthLimit?: number;
    /**
     * Enable or disable automatic retries for transient PostgREST errors.
     * Defaults to `true`.
     */
    retry?: boolean;
  };
  auth?: {
    /**
     * Automatically refreshes the token for logged-in users. Defaults to true.
     */
    autoRefreshToken?: boolean;
    /**
     * Optional key name used for storing tokens in local storage.
     */
    storageKey?: string;
    /**
     * Whether to persist a logged-in session to storage. Defaults to true.
     */
    persistSession?: boolean;
    /**
     * Detect a session from the URL. Used for OAuth login callbacks. Defaults to true.
     *
     * Can be set to a function to provide custom logic for determining if a URL contains
     * a Supabase auth callback. The function receives the current URL and parsed parameters,
     * and should return true if the URL should be processed as a Supabase auth callback.
     *
     * This is useful when your app uses other OAuth providers (e.g., Facebook Login) that
     * also return access_token in the URL fragment, which would otherwise be incorrectly
     * intercepted by Supabase Auth.
     *
     * @example With custom detection logic
     * ```ts
     * detectSessionInUrl: (url, params) => {
     *   // Ignore Facebook OAuth redirects
     *   if (url.pathname === '/facebook/redirect') return false
     *   // Use default detection for other URLs
     *   return Boolean(params.access_token || params.error_description)
     * }
     * ```
     */
    detectSessionInUrl?: boolean | ((url: URL, params: {
      [parameter: string]: string;
    }) => boolean);
    /**
     * A storage provider. Used to store the logged-in session.
     */
    storage?: SupabaseAuthClientOptions['storage'];
    /**
     * A storage provider to store the user profile separately from the session.
     * Useful when you need to store the session information in cookies,
     * without bloating the data with the redundant user object.
     *
     * @experimental
     */
    userStorage?: SupabaseAuthClientOptions['userStorage'];
    /**
     * OAuth flow to use - defaults to implicit flow. PKCE is recommended for mobile and server-side applications.
     */
    flowType?: SupabaseAuthClientOptions['flowType'];
    /**
     * If debug messages for authentication client are emitted. Can be used to inspect the behavior of the library.
     */
    debug?: SupabaseAuthClientOptions['debug'];
    /**
     * Provide your own locking mechanism based on the environment. By default
     * the auth client coordinates refreshes itself and the server resolves
     * cross-tab races. Passing a custom `lock` opts into a legacy path that
     * wraps every auth operation in your supplied lock.
     *
     * @deprecated Custom locks still work in v2.x for backwards compatibility.
     * The legacy lock path will be removed in v3 — drop this option from your
     * `createClient` options before upgrading.
     */
    lock?: SupabaseAuthClientOptions['lock'];
    /**
     * If there is an error with the query, throwOnError will reject the promise by
     * throwing the error instead of returning it as part of a successful response.
     */
    throwOnError?: SupabaseAuthClientOptions['throwOnError'];
    /**
     * Opt-in flags for experimental features. These APIs may change without
     * notice and are disabled by default.
     *
     * @experimental
     */
    experimental?: SupabaseAuthClientOptions['experimental'];
    /**
     * Maximum time in milliseconds to wait for acquiring the custom lock
     * supplied via `lock`. Only consulted when a custom `lock` is passed.
     *
     * @default 5000
     *
     * @deprecated Only used by the legacy lock path. Will be removed in v3
     * along with the `lock` option.
     */
    lockAcquireTimeout?: SupabaseAuthClientOptions['lockAcquireTimeout'];
    /**
     * If true, skips automatic initialization in the auth client constructor.
     * Useful for SSR contexts where initialization timing must be controlled to
     * prevent race conditions with HTTP response generation.
     *
     * @default false
     */
    skipAutoInitialize?: SupabaseAuthClientOptions['skipAutoInitialize'];
  };
  /**
   * Options passed to the realtime-js instance
   */
  realtime?: RealtimeClientOptions;
  storage?: StorageClientOptions;
  global?: {
    /**
     * A custom `fetch` implementation.
     */
    fetch?: Fetch;
    /**
     * Optional headers for initializing the client.
     */
    headers?: Record<string, string>;
  };
  /**
   * Optional function for using a third-party authentication system with
   * Supabase. The function should return an access token or ID token (JWT) by
   * obtaining it from the third-party auth SDK. Note that this
   * function may be called concurrently and many times. Use memoization and
   * locking techniques if this is not supported by the SDKs.
   *
   * When set, the `auth` namespace of the Supabase client cannot be used.
   * Create another client if you wish to use Supabase Auth and third-party
   * authentications concurrently in the same application.
   */
  accessToken?: () => Promise<string | null>;
  /**
   * Enable OpenTelemetry / W3C trace context propagation to Supabase services.
   *
   * Disabled by default. Pass `true` for the common case (auto-detect an
   * active OpenTelemetry context and inject `traceparent` / `tracestate` /
   * `baggage` headers) or an object for fine-grained control.
   *
   * Requires `@opentelemetry/api` to be installed in your application AND
   * the tracing runtime to be loaded with
   * `import '@supabase/supabase-js/tracing'` at your application entry
   * point. Without that import, the SDK logs a one-time warning and sends
   * requests without trace headers. Not available via the CDN/UMD build.
   * Trace headers are only attached to requests targeting Supabase domains,
   * so third-party hosts called through a custom `fetch` are never tagged.
   *
   * The resulting `trace_id` appears in Supabase logs (API Gateway, Edge
   * Functions), letting you correlate client-side spans with server-side
   * log entries — including logs forwarded via Log Drains.
   *
   * @example Shorthand — opt in with defaults
   * ```ts
   * import '@supabase/supabase-js/tracing'
   * import { createClient } from '@supabase/supabase-js'
   *
   * const supabase = createClient(url, key, { tracePropagation: true })
   * ```
   *
   * @example With an active OpenTelemetry span
   * ```ts
   * import '@supabase/supabase-js/tracing'
   * import { createClient } from '@supabase/supabase-js'
   * import { trace } from '@opentelemetry/api'
   *
   * const supabase = createClient(url, key, { tracePropagation: true })
   * const tracer = trace.getTracer('my-app')
   *
   * await tracer.startActiveSpan('fetch-users', async (span) => {
   *   // Request carries the active trace context.
   *   const { data, error } = await supabase.from('users').select('*')
   *   span.end()
   * })
   * ```
   *
   * @example Advanced — always propagate, even for non-sampled traces
   * ```ts
   * import '@supabase/supabase-js/tracing'
   *
   * const supabase = createClient(url, key, {
   *   tracePropagation: { enabled: true, respectSamplingDecision: false },
   * })
   * ```
   *
   * @see https://supabase.com/docs/guides/telemetry/client-side-tracing
   * @see https://www.w3.org/TR/trace-context/
   */
  tracePropagation?: TracePropagationOptions | boolean;
};
/**
 * Helper types for query results.
 */
type QueryResult<T> = T extends PromiseLike<infer U> ? U : never;
type QueryData<T> = T extends PromiseLike<{
  data: infer U;
}> ? Exclude<U, null> : never;
type QueryError = PostgrestError$1;
/**
 * Strips internal Supabase metadata from Database types.
 * Useful for libraries defining generic constraints on Database types.
 *
 * @example Stripping internal Supabase metadata
 * ```typescript
 * type CleanDB = DatabaseWithoutInternals<Database>
 * ```
 */
type DatabaseWithoutInternals<DB> = Omit<DB, '__InternalSupabase'>;
//#endregion
//#region src/lib/helpers.d.ts
type ResolvedSupabaseClientOptions<SchemaName> = Omit<Required<SupabaseClientOptions<SchemaName>>, 'tracePropagation'> & {
  tracePropagation: TracePropagationOptions;
};
//#endregion
//#region src/lib/SupabaseAuthClient.d.ts
declare class SupabaseAuthClient extends AuthClient {
  constructor(options: SupabaseAuthClientOptions);
}
//#endregion
//#region src/lib/rest/types/common/rpc.d.ts
type IsMatchingArgs<FnArgs extends GenericFunction['Args'], PassedArgs extends GenericFunction['Args']> = [FnArgs] extends [Record<PropertyKey, never>] ? PassedArgs extends Record<PropertyKey, never> ? true : false : keyof PassedArgs extends keyof FnArgs ? PassedArgs extends FnArgs ? true : false : false;
type MatchingFunctionArgs<Fn$1 extends GenericFunction, Args extends GenericFunction['Args']> = Fn$1 extends {
  Args: infer A extends GenericFunction['Args'];
} ? IsMatchingArgs<A, Args> extends true ? Fn$1 : never : false;
type FindMatchingFunctionByArgs<FnUnion, Args extends GenericFunction['Args']> = FnUnion extends infer Fn extends GenericFunction ? MatchingFunctionArgs<Fn, Args> : false;
type TablesAndViews<Schema extends GenericSchema> = Schema['Tables'] & Exclude<Schema['Views'], ''>;
type UnionToIntersection<U$1> = (U$1 extends any ? (k: U$1) => void : never) extends ((k: infer I) => void) ? I : never;
type LastOf<T> = UnionToIntersection<T extends any ? () => T : never> extends (() => infer R) ? R : never;
type IsAny<T> = 0 extends 1 & T ? true : false;
type ExactMatch<T, S> = [T] extends [S] ? ([S] extends [T] ? true : false) : false;
type ExtractExactFunction<Fns, Args> = Fns extends infer F ? F extends GenericFunction ? ExactMatch<F['Args'], Args> extends true ? F : never : never : never;
type IsNever<T> = [T] extends [never] ? true : false;
type RpcFunctionNotFound<FnName> = {
  Row: any;
  Result: {
    error: true;
  } & "Couldn't infer function definition matching provided arguments";
  RelationName: FnName;
  Relationships: null;
};
type CrossSchemaError<TableRef extends string> = {
  error: true;
} & `Function returns SETOF from a different schema ('${TableRef}'). Use .overrideTypes<YourReturnType>() to specify the return type explicitly.`;
type GetRpcFunctionFilterBuilderByArgs<Schema extends GenericSchema, FnName extends string & keyof Schema['Functions'], Args> = {
  0: Schema['Functions'][FnName];
  1: IsAny<Schema> extends true ? any : IsNever<Args> extends true ? IsNever<ExtractExactFunction<Schema['Functions'][FnName], Args>> extends true ? LastOf<Schema['Functions'][FnName]> : ExtractExactFunction<Schema['Functions'][FnName], Args> : Args extends Record<PropertyKey, never> ? LastOf<Schema['Functions'][FnName]> : Args extends GenericFunction['Args'] ? IsNever<LastOf<FindMatchingFunctionByArgs<Schema['Functions'][FnName], Args>>> extends true ? LastOf<Schema['Functions'][FnName]> : LastOf<FindMatchingFunctionByArgs<Schema['Functions'][FnName], Args>> : ExtractExactFunction<Schema['Functions'][FnName], Args> extends GenericFunction ? ExtractExactFunction<Schema['Functions'][FnName], Args> : any;
}[1] extends infer Fn ? IsAny<Fn> extends true ? {
  Row: any;
  Result: any;
  RelationName: FnName;
  Relationships: null;
} : Fn extends GenericFunction ? {
  Row: Fn['SetofOptions'] extends GenericSetofOption ? Fn['SetofOptions']['to'] extends keyof TablesAndViews<Schema> ? TablesAndViews<Schema>[Fn['SetofOptions']['to']]['Row'] : Fn['Returns'] extends any[] ? Fn['Returns'][number] extends Record<string, unknown> ? Fn['Returns'][number] : CrossSchemaError<Fn['SetofOptions']['to'] & string> : Fn['Returns'] extends Record<string, unknown> ? Fn['Returns'] : CrossSchemaError<Fn['SetofOptions']['to'] & string> : Fn['Returns'] extends any[] ? Fn['Returns'][number] extends Record<string, unknown> ? Fn['Returns'][number] : never : Fn['Returns'] extends Record<string, unknown> ? Fn['Returns'] : never;
  Result: Fn['SetofOptions'] extends GenericSetofOption ? Fn['SetofOptions']['isSetofReturn'] extends true ? Fn['SetofOptions']['isOneToOne'] extends true ? Fn['Returns'][] : Fn['Returns'] : Fn['Returns'] : Fn['Returns'];
  RelationName: Fn['SetofOptions'] extends GenericSetofOption ? Fn['SetofOptions']['to'] : FnName;
  Relationships: Fn['SetofOptions'] extends GenericSetofOption ? Fn['SetofOptions']['to'] extends keyof Schema['Tables'] ? Schema['Tables'][Fn['SetofOptions']['to']]['Relationships'] : Fn['SetofOptions']['to'] extends keyof Schema['Views'] ? Schema['Views'][Fn['SetofOptions']['to']]['Relationships'] : null : null;
} : Fn extends false ? RpcFunctionNotFound<FnName> : RpcFunctionNotFound<FnName> : RpcFunctionNotFound<FnName>;
//#endregion
//#region src/SupabaseClient.d.ts
/**
 * Supabase Client.
 *
 * An isomorphic Javascript client for interacting with Postgres.
 */
declare class SupabaseClient<Database = any, SchemaNameOrClientOptions extends (string & keyof Omit<Database, '__InternalSupabase'>) | {
  PostgrestVersion: string;
} = ('public' extends keyof Omit<Database, '__InternalSupabase'> ? 'public' : string & keyof Omit<Database, '__InternalSupabase'>), SchemaName extends string & keyof Omit<Database, '__InternalSupabase'> = (SchemaNameOrClientOptions extends string & keyof Omit<Database, '__InternalSupabase'> ? SchemaNameOrClientOptions : 'public' extends keyof Omit<Database, '__InternalSupabase'> ? 'public' : string & keyof Omit<Omit<Database, '__InternalSupabase'>, '__InternalSupabase'>), Schema extends (Omit<Database, '__InternalSupabase'>[SchemaName] extends GenericSchema ? Omit<Database, '__InternalSupabase'>[SchemaName] : never) = (Omit<Database, '__InternalSupabase'>[SchemaName] extends GenericSchema ? Omit<Database, '__InternalSupabase'>[SchemaName] : never), ClientOptions extends {
  PostgrestVersion: string;
} = (SchemaNameOrClientOptions extends string & keyof Omit<Database, '__InternalSupabase'> ? Database extends {
  __InternalSupabase: {
    PostgrestVersion: string;
  };
} ? Database['__InternalSupabase'] : {
  PostgrestVersion: '12';
} : SchemaNameOrClientOptions extends {
  PostgrestVersion: string;
} ? SchemaNameOrClientOptions : never)> {
  protected supabaseUrl: string;
  protected supabaseKey: string;
  /**
   * Supabase Auth allows you to create and manage user sessions for access to data that is secured by access policies.
   */
  auth: SupabaseAuthClient;
  realtime: RealtimeClient;
  /**
   * Supabase Storage allows you to manage user-generated content, such as photos or videos.
   */
  storage: StorageClient;
  protected realtimeUrl: URL;
  protected authUrl: URL;
  protected storageUrl: URL;
  protected functionsUrl: URL;
  protected rest: PostgrestClient<Database, ClientOptions, SchemaName>;
  protected storageKey: string;
  protected fetch?: Fetch;
  protected functionsFetch?: Fetch;
  protected changedAccessToken?: string;
  protected accessToken?: () => Promise<string | null>;
  protected headers: Record<string, string>;
  protected settings?: ResolvedSupabaseClientOptions<SchemaName>;
  /**
   * Create a new client for use in the browser.
   *
   * @category Initializing
   *
   * @param supabaseUrl The unique Supabase URL which is supplied when you create a new project in your project dashboard.
   * @param supabaseKey The unique Supabase Key which is supplied when you create a new project in your project dashboard.
   * @param options Optional configuration for the client:
   * - `db.schema` — You can switch in between schemas. The schema needs to be on the list of exposed schemas inside Supabase.
   * - `auth.autoRefreshToken` — Set to `true` if you want to automatically refresh the token before expiring.
   * - `auth.persistSession` — Set to `true` if you want to automatically save the user session into local storage.
   * - `auth.detectSessionInUrl` — Set to `true` if you want to automatically detect OAuth grants in the URL and sign in the user.
   * - `realtime` — Options passed along to the realtime-js constructor.
   * - `storage` — Options passed along to the storage-js constructor.
   * - `global.fetch` — A custom fetch implementation.
   * - `global.headers` — Any additional headers to send with each network request.
   *
   * @example Creating a client
   * ```js
   * import { createClient } from '@supabase/supabase-js'
   *
   * // Create a single supabase client for interacting with your database
   * const supabase = createClient('https://xyzcompany.supabase.co', 'your-publishable-key')
   * ```
   *
   * @example With a custom domain
   * ```js
   * import { createClient } from '@supabase/supabase-js'
   *
   * // Use a custom domain as the supabase URL
   * const supabase = createClient('https://my-custom-domain.com', 'your-publishable-key')
   * ```
   *
   * @example With additional parameters
   * ```js
   * import { createClient } from '@supabase/supabase-js'
   *
   * const options = {
   *   db: {
   *     schema: 'public',
   *   },
   *   auth: {
   *     autoRefreshToken: true,
   *     persistSession: true,
   *     detectSessionInUrl: true
   *   },
   *   global: {
   *     headers: { 'x-my-custom-header': 'my-app-name' },
   *   },
   * }
   * const supabase = createClient("https://xyzcompany.supabase.co", "your-publishable-key", options)
   * ```
   *
   * @exampleDescription With custom schemas
   * By default the API server points to the `public` schema. You can enable other database schemas within the Dashboard.
   * Go to [Settings > API > Exposed schemas](/dashboard/project/_/settings/api) and add the schema which you want to expose to the API.
   *
   * Note: each client connection can only access a single schema, so the code above can access the `other_schema` schema but cannot access the `public` schema.
   *
   * @example With custom schemas
   * ```js
   * import { createClient } from '@supabase/supabase-js'
   *
   * const supabase = createClient('https://xyzcompany.supabase.co', 'your-publishable-key', {
   *   // Provide a custom schema. Defaults to "public".
   *   db: { schema: 'other_schema' }
   * })
   * ```
   *
   * @exampleDescription Custom fetch implementation
   * `supabase-js` uses the runtime's global `fetch` to make HTTP requests,
   * but an alternative `fetch` implementation can be provided as an option.
   * This is useful in environments where the global `fetch` is unavailable or where you want to customize request behavior.
   *
   * @example Custom fetch implementation
   * ```js
   * import { createClient } from '@supabase/supabase-js'
   *
   * const supabase = createClient('https://xyzcompany.supabase.co', 'your-publishable-key', {
   *   global: { fetch: fetch.bind(globalThis) }
   * })
   * ```
   *
   * @exampleDescription React Native options with AsyncStorage
   * For React Native we recommend using `AsyncStorage` as the storage implementation for Supabase Auth.
   *
   * @example React Native options with AsyncStorage
   * ```js
   * import 'react-native-url-polyfill/auto'
   * import { createClient } from '@supabase/supabase-js'
   * import AsyncStorage from "@react-native-async-storage/async-storage";
   *
   * const supabase = createClient("https://xyzcompany.supabase.co", "your-publishable-key", {
   *   auth: {
   *     storage: AsyncStorage,
   *     autoRefreshToken: true,
   *     persistSession: true,
   *     detectSessionInUrl: false,
   *   },
   * });
   * ```
   *
   * @exampleDescription React Native options with Expo SecureStore
   * If you wish to encrypt the user's session information, you can use `aes-js` and store the encryption key in Expo SecureStore.
   * The `aes-js` library, a reputable JavaScript-only implementation of the AES encryption algorithm in CTR mode.
   * A new 256-bit encryption key is generated using the `react-native-get-random-values` library.
   * This key is stored inside Expo's SecureStore, while the value is encrypted and placed inside AsyncStorage.
   *
   * Please make sure that:
   * - You keep the `expo-secure-store`, `aes-js` and `react-native-get-random-values` libraries up-to-date.
   * - Choose the correct [`SecureStoreOptions`](https://docs.expo.dev/versions/latest/sdk/securestore/#securestoreoptions) for your app's needs.
   *   E.g. [`SecureStore.WHEN_UNLOCKED`](https://docs.expo.dev/versions/latest/sdk/securestore/#securestorewhen_unlocked) regulates when the data can be accessed.
   * - Carefully consider optimizations or other modifications to the above example, as those can lead to introducing subtle security vulnerabilities.
   *
   * @example React Native options with Expo SecureStore
   * ```ts
   * import 'react-native-url-polyfill/auto'
   * import { createClient } from '@supabase/supabase-js'
   * import AsyncStorage from '@react-native-async-storage/async-storage';
   * import * as SecureStore from 'expo-secure-store';
   * import * as aesjs from 'aes-js';
   * import 'react-native-get-random-values';
   *
   * // As Expo's SecureStore does not support values larger than 2048
   * // bytes, an AES-256 key is generated and stored in SecureStore, while
   * // it is used to encrypt/decrypt values stored in AsyncStorage.
   * class LargeSecureStore {
   *   private async _encrypt(key: string, value: string) {
   *     const encryptionKey = crypto.getRandomValues(new Uint8Array(256 / 8));
   *
   *     const cipher = new aesjs.ModeOfOperation.ctr(encryptionKey, new aesjs.Counter(1));
   *     const encryptedBytes = cipher.encrypt(aesjs.utils.utf8.toBytes(value));
   *
   *     await SecureStore.setItemAsync(key, aesjs.utils.hex.fromBytes(encryptionKey));
   *
   *     return aesjs.utils.hex.fromBytes(encryptedBytes);
   *   }
   *
   *   private async _decrypt(key: string, value: string) {
   *     const encryptionKeyHex = await SecureStore.getItemAsync(key);
   *     if (!encryptionKeyHex) {
   *       return encryptionKeyHex;
   *     }
   *
   *     const cipher = new aesjs.ModeOfOperation.ctr(aesjs.utils.hex.toBytes(encryptionKeyHex), new aesjs.Counter(1));
   *     const decryptedBytes = cipher.decrypt(aesjs.utils.hex.toBytes(value));
   *
   *     return aesjs.utils.utf8.fromBytes(decryptedBytes);
   *   }
   *
   *   async getItem(key: string) {
   *     const encrypted = await AsyncStorage.getItem(key);
   *     if (!encrypted) { return encrypted; }
   *
   *     return await this._decrypt(key, encrypted);
   *   }
   *
   *   async removeItem(key: string) {
   *     await AsyncStorage.removeItem(key);
   *     await SecureStore.deleteItemAsync(key);
   *   }
   *
   *   async setItem(key: string, value: string) {
   *     const encrypted = await this._encrypt(key, value);
   *
   *     await AsyncStorage.setItem(key, encrypted);
   *   }
   * }
   *
   * const supabase = createClient("https://xyzcompany.supabase.co", "your-publishable-key", {
   *   auth: {
   *     storage: new LargeSecureStore(),
   *     autoRefreshToken: true,
   *     persistSession: true,
   *     detectSessionInUrl: false,
   *   },
   * });
   * ```
   *
   * @example With a database query
   * ```ts
   * import { createClient } from '@supabase/supabase-js'
   *
   * const supabase = createClient('https://xyzcompany.supabase.co', 'your-publishable-key')
   *
   * const { data } = await supabase.from('profiles').select('*')
   * ```
   *
   * @exampleDescription With OpenTelemetry tracing
   * Opt in to W3C trace context propagation so the `trace_id` from your
   * client-side spans is attached to Supabase requests and appears in API
   * Gateway and Edge Function logs. Requires `@opentelemetry/api` to be
   * installed in your application and the tracing runtime to be loaded via
   * `import '@supabase/supabase-js/tracing'`. See [Tracing with the JS SDK](https://supabase.com/docs/guides/telemetry/client-side-tracing).
   *
   * @example With OpenTelemetry tracing
   * ```ts
   * import '@supabase/supabase-js/tracing'
   * import { createClient } from '@supabase/supabase-js'
   * import { trace } from '@opentelemetry/api'
   *
   * const supabase = createClient('https://xyzcompany.supabase.co', 'your-publishable-key', {
   *   tracePropagation: true,
   * })
   *
   * const tracer = trace.getTracer('my-app')
   *
   * await tracer.startActiveSpan('fetch-users', async (span) => {
   *   // Outgoing request carries the active trace context.
   *   const { data, error } = await supabase.from('users').select('*')
   *   span.end()
   * })
   * ```
   */
  constructor(supabaseUrl: string, supabaseKey: string, options?: SupabaseClientOptions<SchemaName>);
  /**
   * Supabase Functions allows you to deploy and invoke edge functions.
   */
  get functions(): FunctionsClient;
  from<TableName extends string & keyof Schema['Tables'], Table extends Schema['Tables'][TableName]>(relation: TableName): PostgrestQueryBuilder$1<ClientOptions, Schema, Table, TableName>;
  from<ViewName extends string & keyof Schema['Views'], View extends Schema['Views'][ViewName]>(relation: ViewName): PostgrestQueryBuilder$1<ClientOptions, Schema, View, ViewName>;
  /**
   * Select a schema to query or perform an function (rpc) call.
   *
   * The schema needs to be on the list of exposed schemas inside Supabase.
   *
   * @param schema - The schema to query
   */
  schema<DynamicSchema extends string & keyof Omit<Database, '__InternalSupabase'>>(schema: DynamicSchema): PostgrestClient<Database, ClientOptions, DynamicSchema, Database[DynamicSchema] extends GenericSchema ? Database[DynamicSchema] : any>;
  /**
   * Fetch the OpenAPI description PostgREST publishes for this client's schema.
   *
   * The document lists only the tables, views and functions the caller's role
   * holds privileges on. The request carries the same `apikey` and
   * `Authorization` headers as every other query, so the description is scoped
   * to the signed-in user. Call `.schema()` first to describe a schema other
   * than the client default.
   *
   * @example
   * ```ts
   * const { data, error } = await supabase.getOpenApiSpec()
   * ```
   */
  getOpenApiSpec(): Promise<PostgrestSingleResponse$1<PostgrestOpenApiSpec$1>>;
  /**
   * Perform a function call.
   *
   * @param fn - The function name to call
   * @param args - The arguments to pass to the function call
   * @param options - Named parameters
   * @param options.head - When set to `true`, `data` will not be returned.
   * Useful if you only need the count.
   * @param options.get - When set to `true`, the function will be called with
   * read-only access mode.
   * @param options.count - Count algorithm to use to count rows returned by the
   * function. Only applicable for [set-returning
   * functions](https://www.postgresql.org/docs/current/functions-srf.html).
   *
   * `"exact"`: Exact but slow count algorithm. Performs a `COUNT(*)` under the
   * hood.
   *
   * `"planned"`: Approximated but fast count algorithm. Uses the Postgres
   * statistics under the hood.
   *
   * `"estimated"`: Uses exact count for low numbers and planned count for high
   * numbers.
   */
  rpc<FnName extends string & keyof Schema['Functions'], Args extends Schema['Functions'][FnName]['Args'] = never, FilterBuilder extends GetRpcFunctionFilterBuilderByArgs<Schema, FnName, Args> = GetRpcFunctionFilterBuilderByArgs<Schema, FnName, Args>>(fn: FnName, args?: Args, options?: {
    head?: boolean;
    get?: boolean;
    count?: 'exact' | 'planned' | 'estimated';
  }): PostgrestFilterBuilder$1<ClientOptions, Schema, FilterBuilder['Row'], FilterBuilder['Result'], FilterBuilder['RelationName'], FilterBuilder['Relationships'], 'RPC'>;
  /**
   * Creates a Realtime channel with Broadcast, Presence, and Postgres Changes.
   *
   * @param {string} name - The name of the Realtime channel.
   * @param {Object} opts - The options to pass to the Realtime channel.
   *
   * @category Realtime
   */
  channel(name: string, opts?: RealtimeChannelOptions): RealtimeChannel;
  /**
   * Returns all Realtime channels.
   *
   * @category Realtime
   *
   * @example Get all channels
   * ```js
   * const channels = supabase.getChannels()
   * ```
   */
  getChannels(): RealtimeChannel[];
  /**
   * Unsubscribes and removes Realtime channel from Realtime client.
   *
   * @param {RealtimeChannel} channel - The name of the Realtime channel.
   *
   *
   * @category Realtime
   *
   * @remarks
   * - Removing a channel is a great way to maintain the performance of your project's Realtime service as well as your database if you're listening to Postgres changes. Supabase will automatically handle cleanup 30 seconds after a client is disconnected, but unused channels may cause degradation as more clients are simultaneously subscribed.
   *
   * @example Removes a channel
   * ```js
   * supabase.removeChannel(myChannel)
   * ```
   */
  removeChannel(channel: RealtimeChannel): Promise<RealtimeRemoveChannelResponse>;
  /**
   * Unsubscribes and removes all Realtime channels from Realtime client.
   *
   * @category Realtime
   *
   * @remarks
   * - Removing channels is a great way to maintain the performance of your project's Realtime service as well as your database if you're listening to Postgres changes. Supabase will automatically handle cleanup 30 seconds after a client is disconnected, but unused channels may cause degradation as more clients are simultaneously subscribed.
   *
   * @example Remove all channels
   * ```js
   * supabase.removeAllChannels()
   * ```
   */
  removeAllChannels(): Promise<RealtimeRemoveChannelResponse[]>;
  /**
   * The raw session token — the custom `accessToken` result or the signed-in user's JWT —
   * or `null` when there is no session. Unlike {@link _getAccessToken} it does not fall back
   * to `supabaseKey`, so callers can distinguish "no session" from "has session".
   */
  private _getSessionToken;
  private _getAccessToken;
  private _initSupabaseAuthClient;
  private _initRealtimeClient;
  private _listenForAuthEvents;
  private _handleTokenChanged;
}
//#endregion
//#region src/index.d.ts
/**
 * Creates a new Supabase Client.
 *
 * @example Creating a Supabase client
 * ```ts
 * import { createClient } from '@supabase/supabase-js'
 *
 * const supabase = createClient('https://xyzcompany.supabase.co', 'your-publishable-key')
 * const { data, error } = await supabase.from('profiles').select('*')
 * ```
 */
declare const createClient: <Database = any, SchemaNameOrClientOptions extends (string & keyof Omit<Database, "__InternalSupabase">) | {
  PostgrestVersion: string;
} = ("public" extends keyof Omit<Database, "__InternalSupabase"> ? "public" : string & keyof Omit<Database, "__InternalSupabase">), SchemaName extends string & keyof Omit<Database, "__InternalSupabase"> = (SchemaNameOrClientOptions extends string & keyof Omit<Database, "__InternalSupabase"> ? SchemaNameOrClientOptions : "public" extends keyof Omit<Database, "__InternalSupabase"> ? "public" : string & keyof Omit<Omit<Database, "__InternalSupabase">, "__InternalSupabase">)>(supabaseUrl: string, supabaseKey: string, options?: SupabaseClientOptions<SchemaName>) => SupabaseClient<Database, SchemaNameOrClientOptions, SchemaName>;
//#endregion
export { type AuthSession, type AuthUser, type DatabaseWithoutInternals, type FunctionInvokeOptions, FunctionRegion, FunctionsError, FunctionsFetchError, FunctionsHttpError, FunctionsRelayError, type PostgrestBuilder, PostgrestError, type PostgrestFilterBuilder, type PostgrestMaybeSingleResponse, type PostgrestOpenApiSpec, type PostgrestQueryBuilder, type PostgrestResponse, type PostgrestSingleResponse, type PostgrestTransformBuilder, type QueryData, type QueryError, type QueryResult, StorageApiError, SupabaseClient, type SupabaseClientOptions, type TracePropagationOptions, createClient };
//# sourceMappingURL=index.d.cts.map