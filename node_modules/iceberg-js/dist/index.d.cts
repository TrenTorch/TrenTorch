type AuthConfig = {
    type: 'none';
} | {
    type: 'bearer';
    token: string;
} | {
    type: 'header';
    name: string;
    value: string;
} | {
    type: 'custom';
    getHeaders: () => Record<string, string> | Promise<Record<string, string>>;
};

interface NamespaceIdentifier {
    namespace: string[];
}
interface NamespaceMetadata {
    properties: Record<string, string>;
}
interface TableIdentifier {
    namespace: string[];
    name: string;
}
/**
 * Primitive types in Iceberg - all represented as strings.
 * Parameterized types use string format: decimal(precision,scale) and fixed[length]
 *
 * Note: The OpenAPI spec defines PrimitiveType as `type: string`, so any string is valid.
 * We include known types for autocomplete, plus a catch-all for flexibility.
 */
type PrimitiveType = 'boolean' | 'int' | 'long' | 'float' | 'double' | 'string' | 'timestamp' | 'date' | 'time' | 'timestamptz' | 'uuid' | 'binary' | `decimal(${number},${number})` | `fixed[${number}]` | (string & {});
/**
 * Parse a decimal type string into its components.
 * Handles any whitespace formatting (e.g., "decimal(10,2)", "decimal(10, 2)", "decimal( 10 , 2 )").
 *
 * @param type - The type string to parse
 * @returns Object with precision and scale, or null if not a valid decimal type
 */
declare function parseDecimalType(type: string): {
    precision: number;
    scale: number;
} | null;
/**
 * Parse a fixed type string into its length.
 * Handles any whitespace formatting (e.g., "fixed[16]", "fixed[ 16 ]").
 *
 * @param type - The type string to parse
 * @returns Object with length, or null if not a valid fixed type
 */
declare function parseFixedType(type: string): {
    length: number;
} | null;
/**
 * Check if a type string is a decimal type.
 */
declare function isDecimalType(type: string): boolean;
/**
 * Check if a type string is a fixed type.
 */
declare function isFixedType(type: string): boolean;
/**
 * Compare two Iceberg type strings for equality, ignoring whitespace differences.
 * This is useful when comparing types from user input vs catalog responses,
 * as catalogs may normalize whitespace differently.
 *
 * @param a - First type string
 * @param b - Second type string
 * @returns true if the types are equivalent
 */
declare function typesEqual(a: string, b: string): boolean;
/**
 * Struct type - a nested structure containing fields.
 * Used for nested records within a field.
 */
interface StructType {
    type: 'struct';
    fields: StructField[];
}
/**
 * List type - an array of elements.
 */
interface ListType {
    type: 'list';
    'element-id': number;
    element: IcebergType;
    'element-required': boolean;
}
/**
 * Map type - a key-value mapping.
 */
interface MapType {
    type: 'map';
    'key-id': number;
    key: IcebergType;
    'value-id': number;
    value: IcebergType;
    'value-required': boolean;
}
/**
 * Union of all Iceberg types.
 * Can be a primitive type (string) or a complex type (struct, list, map).
 */
type IcebergType = PrimitiveType | StructType | ListType | MapType;
/**
 * Primitive type values for default values.
 * Represents the possible values for initial-default and write-default.
 */
type PrimitiveTypeValue = boolean | number | string;
/**
 * A field within a struct (used in nested StructType).
 */
interface StructField {
    id: number;
    name: string;
    type: IcebergType;
    required: boolean;
    doc?: string;
    'initial-default'?: PrimitiveTypeValue;
    'write-default'?: PrimitiveTypeValue;
}
/**
 * A field within a table schema (top-level).
 * Equivalent to StructField but kept for backwards compatibility.
 */
interface TableField {
    id: number;
    name: string;
    type: IcebergType;
    required: boolean;
    doc?: string;
    'initial-default'?: PrimitiveTypeValue;
    'write-default'?: PrimitiveTypeValue;
}
interface TableSchema {
    type: 'struct';
    fields: TableField[];
    'schema-id'?: number;
    'identifier-field-ids'?: number[];
}
interface PartitionField {
    source_id: number;
    field_id: number;
    name: string;
    transform: string;
}
interface PartitionSpec {
    'spec-id': number;
    fields: PartitionField[];
}
interface SortField {
    source_id: number;
    transform: string;
    direction: 'asc' | 'desc';
    null_order: 'nulls-first' | 'nulls-last';
}
interface SortOrder {
    'order-id': number;
    fields: SortField[];
}
interface CreateTableRequest {
    name: string;
    schema: TableSchema;
    'partition-spec'?: PartitionSpec;
    'write-order'?: SortOrder;
    properties?: Record<string, string>;
    'stage-create'?: boolean;
}
interface UpdateTableRequest {
    schema?: TableSchema;
    'partition-spec'?: PartitionSpec;
    properties?: Record<string, string>;
}
interface DropTableRequest {
    purge?: boolean;
}
interface TableMetadata {
    name?: string;
    location: string;
    schemas: TableSchema[];
    'current-schema-id': number;
    'partition-specs': PartitionSpec[];
    'default-spec-id'?: number;
    'sort-orders': SortOrder[];
    'default-sort-order-id'?: number;
    properties: Record<string, string>;
    'metadata-location'?: string;
    'current-snapshot-id'?: number;
    snapshots?: unknown[];
    'snapshot-log'?: unknown[];
    'metadata-log'?: unknown[];
    refs?: Record<string, unknown>;
    'last-updated-ms'?: number;
    'last-column-id'?: number;
    'last-sequence-number'?: number;
    'table-uuid'?: string;
    'format-version'?: number;
    'last-partition-id'?: number;
}
interface CreateNamespaceResponse {
    namespace: string[];
    properties?: Record<string, string>;
}
interface CommitTableResponse {
    'metadata-location': string;
    metadata: TableMetadata;
}
/**
 * Gets the current (active) schema from table metadata.
 *
 * @param metadata - Table metadata containing schemas array and current-schema-id
 * @returns The current table schema, or undefined if not found
 */
declare function getCurrentSchema(metadata: TableMetadata): TableSchema | undefined;

/**
 * Access delegation mechanisms supported by the Iceberg REST Catalog.
 *
 * - `vended-credentials`: Server provides temporary credentials for data access
 * - `remote-signing`: Server signs requests on behalf of the client
 */
type AccessDelegation = 'vended-credentials' | 'remote-signing';
/**
 * Configuration options for the Iceberg REST Catalog client.
 */
interface IcebergRestCatalogOptions {
    /** Base URL of the Iceberg REST Catalog API */
    baseUrl: string;
    /** Optional catalog name prefix for multi-catalog servers */
    catalogName?: string;
    /** Authentication configuration */
    auth?: AuthConfig;
    /** Custom fetch implementation (defaults to globalThis.fetch) */
    fetch?: typeof fetch;
    /**
     * Access delegation mechanisms to request from the server.
     * When specified, the X-Iceberg-Access-Delegation header will be sent
     * with supported operations (createTable, loadTable).
     *
     * @example ['vended-credentials']
     * @example ['vended-credentials', 'remote-signing']
     */
    accessDelegation?: AccessDelegation[];
}
/**
 * Client for interacting with an Apache Iceberg REST Catalog.
 *
 * This class provides methods for managing namespaces and tables in an Iceberg catalog.
 * It handles authentication, request formatting, and error handling automatically.
 *
 * @example
 * ```typescript
 * const catalog = new IcebergRestCatalog({
 *   baseUrl: 'https://my-catalog.example.com/iceberg/v1',
 *   auth: { type: 'bearer', token: process.env.ICEBERG_TOKEN }
 * });
 *
 * // Create a namespace
 * await catalog.createNamespace({ namespace: ['analytics'] });
 *
 * // Create a table
 * await catalog.createTable(
 *   { namespace: ['analytics'] },
 *   {
 *     name: 'events',
 *     schema: { type: 'struct', fields: [...] }
 *   }
 * );
 * ```
 */
declare class IcebergRestCatalog {
    private readonly client;
    private readonly namespaceOps;
    private readonly tableOps;
    private readonly accessDelegation?;
    /**
     * Creates a new Iceberg REST Catalog client.
     *
     * @param options - Configuration options for the catalog client
     */
    constructor(options: IcebergRestCatalogOptions);
    /**
     * Lists all namespaces in the catalog.
     *
     * @param parent - Optional parent namespace to list children under
     * @returns Array of namespace identifiers
     *
     * @example
     * ```typescript
     * // List all top-level namespaces
     * const namespaces = await catalog.listNamespaces();
     *
     * // List namespaces under a parent
     * const children = await catalog.listNamespaces({ namespace: ['analytics'] });
     * ```
     */
    listNamespaces(parent?: NamespaceIdentifier): Promise<NamespaceIdentifier[]>;
    /**
     * Creates a new namespace in the catalog.
     *
     * @param id - Namespace identifier to create
     * @param metadata - Optional metadata properties for the namespace
     * @returns Response containing the created namespace and its properties
     *
     * @example
     * ```typescript
     * const response = await catalog.createNamespace(
     *   { namespace: ['analytics'] },
     *   { properties: { owner: 'data-team' } }
     * );
     * console.log(response.namespace); // ['analytics']
     * console.log(response.properties); // { owner: 'data-team', ... }
     * ```
     */
    createNamespace(id: NamespaceIdentifier, metadata?: NamespaceMetadata): Promise<CreateNamespaceResponse>;
    /**
     * Drops a namespace from the catalog.
     *
     * The namespace must be empty (contain no tables) before it can be dropped.
     *
     * @param id - Namespace identifier to drop
     *
     * @example
     * ```typescript
     * await catalog.dropNamespace({ namespace: ['analytics'] });
     * ```
     */
    dropNamespace(id: NamespaceIdentifier): Promise<void>;
    /**
     * Loads metadata for a namespace.
     *
     * @param id - Namespace identifier to load
     * @returns Namespace metadata including properties
     *
     * @example
     * ```typescript
     * const metadata = await catalog.loadNamespaceMetadata({ namespace: ['analytics'] });
     * console.log(metadata.properties);
     * ```
     */
    loadNamespaceMetadata(id: NamespaceIdentifier): Promise<NamespaceMetadata>;
    /**
     * Lists all tables in a namespace.
     *
     * @param namespace - Namespace identifier to list tables from
     * @returns Array of table identifiers
     *
     * @example
     * ```typescript
     * const tables = await catalog.listTables({ namespace: ['analytics'] });
     * console.log(tables); // [{ namespace: ['analytics'], name: 'events' }, ...]
     * ```
     */
    listTables(namespace: NamespaceIdentifier): Promise<TableIdentifier[]>;
    /**
     * Creates a new table in the catalog.
     *
     * @param namespace - Namespace to create the table in
     * @param request - Table creation request including name, schema, partition spec, etc.
     * @returns Table metadata for the created table
     *
     * @example
     * ```typescript
     * const metadata = await catalog.createTable(
     *   { namespace: ['analytics'] },
     *   {
     *     name: 'events',
     *     schema: {
     *       type: 'struct',
     *       fields: [
     *         { id: 1, name: 'id', type: 'long', required: true },
     *         { id: 2, name: 'timestamp', type: 'timestamp', required: true }
     *       ],
     *       'schema-id': 0
     *     },
     *     'partition-spec': {
     *       'spec-id': 0,
     *       fields: [
     *         { source_id: 2, field_id: 1000, name: 'ts_day', transform: 'day' }
     *       ]
     *     }
     *   }
     * );
     * ```
     */
    createTable(namespace: NamespaceIdentifier, request: CreateTableRequest): Promise<TableMetadata>;
    /**
     * Updates an existing table's metadata.
     *
     * Can update the schema, partition spec, or properties of a table.
     *
     * @param id - Table identifier to update
     * @param request - Update request with fields to modify
     * @returns Response containing the metadata location and updated table metadata
     *
     * @example
     * ```typescript
     * const response = await catalog.updateTable(
     *   { namespace: ['analytics'], name: 'events' },
     *   {
     *     properties: { 'read.split.target-size': '134217728' }
     *   }
     * );
     * console.log(response['metadata-location']); // s3://...
     * console.log(response.metadata); // TableMetadata object
     * ```
     */
    updateTable(id: TableIdentifier, request: UpdateTableRequest): Promise<CommitTableResponse>;
    /**
     * Drops a table from the catalog.
     *
     * @param id - Table identifier to drop
     *
     * @example
     * ```typescript
     * await catalog.dropTable({ namespace: ['analytics'], name: 'events' });
     * ```
     */
    dropTable(id: TableIdentifier, options?: DropTableRequest): Promise<void>;
    /**
     * Loads metadata for a table.
     *
     * @param id - Table identifier to load
     * @returns Table metadata including schema, partition spec, location, etc.
     *
     * @example
     * ```typescript
     * const metadata = await catalog.loadTable({ namespace: ['analytics'], name: 'events' });
     * console.log(metadata.schema);
     * console.log(metadata.location);
     * ```
     */
    loadTable(id: TableIdentifier): Promise<TableMetadata>;
    /**
     * Checks if a namespace exists in the catalog.
     *
     * @param id - Namespace identifier to check
     * @returns True if the namespace exists, false otherwise
     *
     * @example
     * ```typescript
     * const exists = await catalog.namespaceExists({ namespace: ['analytics'] });
     * console.log(exists); // true or false
     * ```
     */
    namespaceExists(id: NamespaceIdentifier): Promise<boolean>;
    /**
     * Checks if a table exists in the catalog.
     *
     * @param id - Table identifier to check
     * @returns True if the table exists, false otherwise
     *
     * @example
     * ```typescript
     * const exists = await catalog.tableExists({ namespace: ['analytics'], name: 'events' });
     * console.log(exists); // true or false
     * ```
     */
    tableExists(id: TableIdentifier): Promise<boolean>;
    /**
     * Creates a namespace if it does not exist.
     *
     * If the namespace already exists, returns void. If created, returns the response.
     *
     * @param id - Namespace identifier to create
     * @param metadata - Optional metadata properties for the namespace
     * @returns Response containing the created namespace and its properties, or void if it already exists
     *
     * @example
     * ```typescript
     * const response = await catalog.createNamespaceIfNotExists(
     *   { namespace: ['analytics'] },
     *   { properties: { owner: 'data-team' } }
     * );
     * if (response) {
     *   console.log('Created:', response.namespace);
     * } else {
     *   console.log('Already exists');
     * }
     * ```
     */
    createNamespaceIfNotExists(id: NamespaceIdentifier, metadata?: NamespaceMetadata): Promise<CreateNamespaceResponse | void>;
    /**
     * Creates a table if it does not exist.
     *
     * If the table already exists, returns its metadata instead.
     *
     * @param namespace - Namespace to create the table in
     * @param request - Table creation request including name, schema, partition spec, etc.
     * @returns Table metadata for the created or existing table
     *
     * @example
     * ```typescript
     * const metadata = await catalog.createTableIfNotExists(
     *   { namespace: ['analytics'] },
     *   {
     *     name: 'events',
     *     schema: {
     *       type: 'struct',
     *       fields: [
     *         { id: 1, name: 'id', type: 'long', required: true },
     *         { id: 2, name: 'timestamp', type: 'timestamp', required: true }
     *       ],
     *       'schema-id': 0
     *     }
     *   }
     * );
     * ```
     */
    createTableIfNotExists(namespace: NamespaceIdentifier, request: CreateTableRequest): Promise<TableMetadata>;
}

interface IcebergErrorResponse {
    error: {
        message: string;
        type: string;
        code: number;
        stack?: string[];
    };
}
declare class IcebergError extends Error {
    readonly status: number;
    readonly icebergType?: string;
    readonly icebergCode?: number;
    readonly details?: unknown;
    readonly isCommitStateUnknown: boolean;
    constructor(message: string, opts: {
        status: number;
        icebergType?: string;
        icebergCode?: number;
        details?: unknown;
    });
    /**
     * Returns true if the error is a 404 Not Found error.
     */
    isNotFound(): boolean;
    /**
     * Returns true if the error is a 409 Conflict error.
     */
    isConflict(): boolean;
    /**
     * Returns true if the error is a 419 Authentication Timeout error.
     */
    isAuthenticationTimeout(): boolean;
}

export { type AccessDelegation, type AuthConfig, type CommitTableResponse, type CreateNamespaceResponse, type CreateTableRequest, type DropTableRequest, IcebergError, type IcebergErrorResponse, IcebergRestCatalog, type IcebergRestCatalogOptions, type IcebergType, type ListType, type MapType, type NamespaceIdentifier, type NamespaceMetadata, type PartitionField, type PartitionSpec, type PrimitiveType, type PrimitiveTypeValue, type SortField, type SortOrder, type StructField, type StructType, type TableField, type TableIdentifier, type TableMetadata, type TableSchema, type UpdateTableRequest, getCurrentSchema, isDecimalType, isFixedType, parseDecimalType, parseFixedType, typesEqual };
