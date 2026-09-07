import { IcebergError, IcebergRestCatalog } from "iceberg-js";

//#region src/lib/common/errors.d.ts

/**
 * Namespace type for error classes
 * Determines the error class names and type guards
 */
type ErrorNamespace = 'storage' | 'vectors';
/**
 * Base error class for all Storage errors
 * Supports both 'storage' and 'vectors' namespaces
 */
declare class StorageError extends Error {
  protected __isStorageError: boolean;
  protected namespace: ErrorNamespace;
  status: number | undefined;
  statusCode: string | undefined;
  constructor(message: string, namespace?: ErrorNamespace, status?: number, statusCode?: string);
  toJSON(): {
    name: string;
    message: string;
    status: number | undefined;
    statusCode: string | undefined;
  };
}
/**
 * Type guard to check if an error is a StorageError
 * @param error - The error to check
 * @returns True if the error is a StorageError
 */
declare function isStorageError(error: unknown): error is StorageError;
/**
 * API error returned from Storage service
 * Includes HTTP status code and service-specific error code
 */
declare class StorageApiError extends StorageError {
  status: number;
  statusCode: string;
  /**
   * Service-specific error code from the Storage API response body, such as
   * `NoSuchKey`, `AccessDenied` or `ResourceAlreadyExists`. Use this to branch
   * on the specific error rather than parsing the message.
   * @see https://supabase.com/docs/guides/storage/debugging/error-codes
   */
  code: string | undefined;
  constructor(message: string, status: number, statusCode: string, namespace?: ErrorNamespace, code?: string);
  toJSON(): {
    name: string;
    message: string;
    status: number | undefined;
    statusCode: string | undefined;
    code: string | undefined;
  };
}
/**
 * Unknown error that doesn't match expected error patterns
 * Wraps the original error for debugging
 */
declare class StorageUnknownError extends StorageError {
  originalError: unknown;
  constructor(message: string, originalError: unknown, namespace?: ErrorNamespace);
}
/**
 * @deprecated Use StorageError with namespace='vectors' instead
 * Alias for backward compatibility with existing vector storage code
 */
declare class StorageVectorsError extends StorageError {
  constructor(message: string);
}
/**
 * Type guard to check if an error is a StorageVectorsError
 * @param error - The error to check
 * @returns True if the error is a StorageVectorsError
 */
declare function isStorageVectorsError(error: unknown): error is StorageVectorsError;
/**
 * @deprecated Use StorageApiError with namespace='vectors' instead
 * Alias for backward compatibility with existing vector storage code
 */
declare class StorageVectorsApiError extends StorageApiError {
  constructor(message: string, status: number, statusCode: string);
}
/**
 * @deprecated Use StorageUnknownError with namespace='vectors' instead
 * Alias for backward compatibility with existing vector storage code
 */
declare class StorageVectorsUnknownError extends StorageUnknownError {
  constructor(message: string, originalError: unknown);
}
/**
 * Error codes specific to S3 Vectors API
 * Maps AWS service errors to application-friendly error codes
 */
declare enum StorageVectorsErrorCode {
  /** Internal server fault (HTTP 500) */
  InternalError = "InternalError",
  /** Resource already exists / conflict (HTTP 409) */
  S3VectorConflictException = "S3VectorConflictException",
  /** Resource not found (HTTP 404) */
  S3VectorNotFoundException = "S3VectorNotFoundException",
  /** Delete bucket while not empty (HTTP 400) */
  S3VectorBucketNotEmpty = "S3VectorBucketNotEmpty",
  /** Exceeds bucket quota/limit (HTTP 400) */
  S3VectorMaxBucketsExceeded = "S3VectorMaxBucketsExceeded",
  /** Exceeds index quota/limit (HTTP 400) */
  S3VectorMaxIndexesExceeded = "S3VectorMaxIndexesExceeded",
}
//#endregion
//#region src/lib/types.d.ts
/**
 * Type of storage bucket
 * - STANDARD: Regular file storage buckets
 * - ANALYTICS: Iceberg table-based buckets for analytical workloads
 */
type BucketType = 'STANDARD' | 'ANALYTICS' | (string & {});
/**
 * Bucket-level object versioning status, as reported by the API.
 * - DISABLED: versioning has never been enabled for the bucket (the implicit starting state)
 * - ENABLED: new object writes create new versions
 * - SUSPENDED: versioning was enabled, then suspended
 */
type VersioningStatus = 'DISABLED' | 'ENABLED' | 'SUSPENDED';
/**
 * Bucket-level object versioning status that can be set via `createBucket`.
 * `SUSPENDED` is excluded: it only makes sense for a bucket that has already
 * had versioning enabled at some point - a brand-new bucket with no history
 * should just start `DISABLED` instead.
 */
type CreateSettableVersioningStatus = Exclude<VersioningStatus, 'SUSPENDED'>;
/**
 * Bucket-level object versioning status that can be set via `updateBucket`.
 * `DISABLED` is excluded: it's never a legal destination, since there's no
 * transition back to it once versioning has been touched.
 */
type UpdateSettableVersioningStatus = Exclude<VersioningStatus, 'DISABLED'>;
/**
 * Whether a lifecycle rule runs.
 * `Enabled` applies the rule. `Disabled` keeps it stored but inactive.
 */
type LifecycleRuleStatus = 'Enabled' | 'Disabled';
/**
 * When to expire noncurrent object versions (previous versions of an object).
 *
 * `noncurrentDays` is how old a noncurrent version must be before it can
 * expire. `newerNoncurrentVersions` keeps that many of the newest noncurrent
 * versions regardless of age, then expires the rest. Allowed range is 1 to 100.
 */
interface NoncurrentVersionExpiration {
  noncurrentDays: number;
  newerNoncurrentVersions?: number;
}
/**
 * Object filter for a lifecycle rule.
 *
 * Currently only `{}` is accepted. Prefix, tag, and size filters are rejected.
 */
type LifecycleRuleFilter = Record<string, never>;
/**
 * One lifecycle rule.
 *
 * Today the only action is `noncurrentVersionExpiration`. `filter` is required
 * and must be `{}`. `id` is optional. The server generates one if you omit it.
 */
interface LifecycleRule {
  id?: string;
  status: LifecycleRuleStatus;
  filter: LifecycleRuleFilter;
  noncurrentVersionExpiration: NoncurrentVersionExpiration;
}
/**
 * Lifecycle policy stored on a bucket.
 * 1 to 1000 rules. Rule IDs must be unique when you set them.
 */
interface BucketLifecycleConfiguration {
  rules: LifecycleRule[];
}
interface Bucket {
  id: string;
  type?: BucketType;
  name: string;
  owner: string;
  file_size_limit?: number;
  allowed_mime_types?: string[];
  created_at: string;
  updated_at: string;
  public: boolean;
  versioning_status?: VersioningStatus;
}
interface ListBucketOptions {
  limit?: number;
  offset?: number;
  sortColumn?: 'id' | 'name' | 'created_at' | 'updated_at';
  sortOrder?: 'asc' | 'desc';
  search?: string;
}
interface PurgeCacheOptions {
  /**
   * If true, purges only the transformations (resized/formatted variants) for the object or bucket,
   * leaving the original cached file intact. If omitted, purges all cached versions.
   */
  transformations?: true;
}
/**
 * Represents an Analytics Bucket using Apache Iceberg table format.
 * Analytics buckets are optimized for analytical queries and data processing.
 */
interface AnalyticBucket {
  /** Unique identifier for the bucket */
  name: string;
  /** Bucket type - always 'ANALYTICS' for analytics buckets */
  type: 'ANALYTICS';
  /** Storage format used (e.g., 'iceberg') */
  format: string;
  /** ISO 8601 timestamp of bucket creation */
  created_at: string;
  /** ISO 8601 timestamp of last update */
  updated_at: string;
}
/**
 * Metadata object returned by the Storage API for files
 * Contains information about file size, type, caching, and HTTP response details
 */
interface FileMetadata {
  /** Entity tag for caching and conditional requests */
  eTag: string;
  /** File size in bytes */
  size: number;
  /** MIME type of the file */
  mimetype: string;
  /** Cache control directive (e.g., "max-age=3600") */
  cacheControl: string;
  /** Last modification timestamp (ISO 8601) */
  lastModified: string;
  /** Content length in bytes (usually same as size) */
  contentLength: number;
  /** HTTP status code from the storage backend */
  httpStatusCode: number;
  /** Any additional custom metadata stored with the file */
  [key: string]: any;
}
/**
 * File object returned by the List V1 API (list() method)
 * Note: Folder entries will have null values for most fields except name
 *
 * Warning: Some fields may not be present in all API responses. Fields like
 * bucket_id, owner, and buckets are not returned by list() operations.
 */
interface FileObject {
  /** File or folder name (relative to the prefix) - always present */
  name: string;
  /** Unique identifier for the file (null for folders) */
  id: string | null;
  /** Last update timestamp (null for folders) */
  updated_at: string | null;
  /** Creation timestamp (null for folders) */
  created_at: string | null;
  /** @deprecated Last access timestamp (null for folders) */
  last_accessed_at: string | null;
  /** File metadata including size, mimetype, etc. (null for folders) */
  metadata: FileMetadata | null;
  /**
   * @deprecated Bucket identifier - NOT returned by list() operations.
   * May be present in remove() responses. Do not rely on this field.
   */
  bucket_id?: string;
  /**
   * @deprecated Owner identifier - NOT returned by list() or remove() operations.
   * This field should not be relied upon.
   */
  owner?: string;
  /**
   * @deprecated Bucket object - NOT returned by list() or remove() operations.
   * This field should not be relied upon.
   */
  buckets?: Bucket;
  /** Version identifier for this object (null for folders, omitted on older schemas) */
  version?: string | null;
  /** Timestamp at which this version was archived */
  archived_at?: string | null;
  /** Whether this entry is a delete marker rather than a real object version (null for folders, omitted on older schemas) */
  is_delete_marker?: boolean | null;
  /** Whether this object was created while the bucket had versioning enabled (null for folders, omitted on older schemas) */
  is_versioned?: boolean | null;
}
/**
 * File object returned by the Info endpoint (info() method)
 * Contains detailed metadata for a specific file
 */
interface FileObjectV2 {
  /** Unique identifier for the file */
  id: string;
  /** File version identifier */
  version: string;
  /** File name */
  name: string;
  /** Bucket identifier */
  bucket_id: string;
  /** Creation timestamp */
  created_at: string;
  /** File size in bytes */
  size?: number;
  /** Cache control header value */
  cache_control?: string;
  /** MIME content type */
  content_type?: string;
  /** Entity tag for caching */
  etag?: string;
  /** Last modification timestamp (replaces updated_at) */
  last_modified?: string;
  /** Custom file metadata */
  metadata?: FileMetadata;
  /**
   * @deprecated The API returns last_modified instead.
   * This field may not be present in responses.
   */
  updated_at?: string;
  /** Timestamp at which this version was archived */
  archived_at?: string | null;
  /** Whether this entry is a delete marker rather than a real object version */
  is_delete_marker?: boolean;
  /** Whether this object was created while the bucket had versioning enabled */
  is_versioned?: boolean;
}
interface SortBy {
  column?: string;
  order?: string;
}
interface FileOptions {
  /**
   * The number of seconds the asset is cached in the browser and in the Supabase CDN. This is set in the `Cache-Control: max-age=<seconds>` header. Defaults to 3600 seconds.
   */
  cacheControl?: string;
  /**
   * the `Content-Type` header value. Should be specified if using a `fileBody` that is neither `Blob` nor `File` nor `FormData`, otherwise will default to `text/plain;charset=UTF-8`.
   */
  contentType?: string;
  /**
   * When upsert is set to true, the file is overwritten if it exists. When set to false, an error is thrown if the object already exists. Defaults to false.
   */
  upsert?: boolean;
  /**
   * The duplex option is a string parameter that enables or disables duplex streaming, allowing for both reading and writing data in the same stream. It can be passed as an option to the fetch() method.
   */
  duplex?: string;
  /**
   * The metadata option is an object that allows you to store additional information about the file. This information can be used to filter and search for files. The metadata object can contain any key-value pairs you want to store.
   */
  metadata?: Record<string, any>;
  /**
   * Optionally add extra headers
   */
  headers?: Record<string, string>;
}
/**
 * An entry for `remove()`. Either a plain path (deletes whichever row is currently
 * at that path), or an object targeting an exact `(path, versionId)`
 */
type DeleteObjectEntry = string | {
  path: string;
  versionId: string;
};
interface DestinationOptions {
  destinationBucket?: string;
  /**
   * The version id of the source object to move/restore.
   */
  sourceVersionId?: string;
}
interface SearchOptions {
  /**
   * The number of files you want to be returned.
   * @default 100
   */
  limit?: number;
  /**
   * The starting position.
   */
  offset?: number;
  /**
   * The column to sort by. Can be any column inside a FileObject.
   */
  sortBy?: SortBy;
  /**
   * The search string to filter files by.
   */
  search?: string;
  /**
   * Controls whether noncurrent object versions are included in the results.
   * @default 'exclude'
   */
  noncurrentVersions?: 'exclude' | 'include' | 'only';
  /**
   * Controls whether delete markers are included in the results.
   * @default 'exclude'
   */
  deleteMarkers?: 'exclude' | 'include' | 'only';
  /**
   * When true, only returns objects whose key exactly matches the given prefix.
   */
  exactMatch?: boolean;
}
interface SortByV2 {
  column: 'name' | 'updated_at' | 'created_at';
  order?: 'asc' | 'desc';
}
interface SearchV2Options {
  /**
   * The number of files you want to be returned.
   * @default 1000
   */
  limit?: number;
  /**
   * The prefix search string to filter files by.
   */
  prefix?: string;
  /**
   * The cursor used for pagination. Pass the value received from nextCursor of the previous request.
   */
  cursor?: string;
  /**
   * Whether to emulate a hierarchical listing of objects using delimiters.
   *
   * - When `false` (default), all objects are listed as flat key/value pairs.
   * - When `true`, the response groups objects by delimiter, making it appear
   *   like a file/folder hierarchy.
   *
   * @default false
   */
  with_delimiter?: boolean;
  /**
   * The column and order to sort by
   * @default 'name asc'
   */
  sortBy?: SortByV2;
  /**
   * Controls whether noncurrent object versions are included in the results.
   * @default 'exclude'
   */
  noncurrentVersions?: 'exclude' | 'include' | 'only';
  /**
   * Controls whether delete markers are included in the results.
   * @default 'exclude'
   */
  deleteMarkers?: 'exclude' | 'include' | 'only';
  /**
   * When true, only returns objects whose key exactly matches the given prefix.
   */
  exactMatch?: boolean;
}
/**
 * File object returned by the List V2 API (listV2() method)
 * Objects and folders are returned in separate arrays - this type represents
 * actual files only. Use SearchV2Folder for folder entries.
 */
interface SearchV2Object {
  /** File name */
  name: string;
  /** Full object key/path */
  key?: string;
  /** Unique identifier for the file */
  id: string;
  /** Last update timestamp */
  updated_at: string;
  /** Creation timestamp */
  created_at: string;
  /** File metadata including size, mimetype, etc. (null if not yet set) */
  metadata: FileMetadata | null;
  /** @deprecated Last access timestamp */
  last_accessed_at: string;
  /** Version identifier for this object */
  version?: string;
  /** Timestamp at which this version was archived */
  archived_at?: string | null;
  /** Whether this entry is a delete marker rather than a real object version */
  is_delete_marker?: boolean;
  /** Whether this object was created while the bucket had versioning enabled */
  is_versioned?: boolean;
}
/**
 * Folder entry returned by the List V2 API (listV2() method) when using with_delimiter: true
 */
interface SearchV2Folder {
  /** Folder name/prefix */
  name: string;
  /** Full folder key/path */
  key?: string;
}
interface SearchV2Result {
  hasNext: boolean;
  folders: SearchV2Folder[];
  objects: SearchV2Object[];
  nextCursor?: string;
}
interface FetchParameters {
  /**
   * Pass in an AbortController's signal to cancel the request.
   */
  signal?: AbortSignal;
  /**
   * Controls how the request interacts with the browser's HTTP cache.
   * - 'default': Use standard cache behavior
   * - 'no-store': Bypass cache entirely (useful in Edge Functions)
   * - 'reload': Bypass cache but update it with response
   * - 'no-cache': Validate with server before using cached response
   * - 'force-cache': Use cache even if stale
   * - 'only-if-cached': Only use cache, fail if not cached
   */
  cache?: 'default' | 'no-store' | 'reload' | 'no-cache' | 'force-cache' | 'only-if-cached';
}
interface Metadata {
  name: string;
}
interface TransformOptions {
  /**
   * The width of the image in pixels.
   */
  width?: number;
  /**
   * The height of the image in pixels.
   */
  height?: number;
  /**
   * The resize mode can be cover, contain or fill. Defaults to cover.
   * Cover resizes the image to maintain it's aspect ratio while filling the entire width and height.
   * Contain resizes the image to maintain it's aspect ratio while fitting the entire image within the width and height.
   * Fill resizes the image to fill the entire width and height. If the object's aspect ratio does not match the width and height, the image will be stretched to fit.
   */
  resize?: 'cover' | 'contain' | 'fill';
  /**
   * Set the quality of the returned image.
   * A number from 20 to 100, with 100 being the highest quality.
   * Defaults to 80
   */
  quality?: number;
  /**
   * Specify the format of the image requested.
   *
   * When using 'origin' we force the format to be the same as the original image.
   * When this option is not passed in, images are optimized to modern image formats like Webp.
   */
  format?: 'origin';
}
type CamelCase<S extends string> = S extends `${infer P1}_${infer P2}${infer P3}` ? `${Lowercase<P1>}${Uppercase<P2>}${CamelCase<P3>}` : S;
type Camelize<T> = { [K in keyof T as CamelCase<Extract<K, string>>]: T[K] };
type DownloadResult<T> = {
  data: T;
  error: null;
} | {
  data: null;
  error: StorageError;
};
/**
 * Configuration for encryption at rest
 * @property kmsKeyArn - ARN of the KMS key used for encryption
 * @property sseType - Server-side encryption type (e.g., 'KMS')
 */
interface EncryptionConfiguration {
  kmsKeyArn?: string;
  sseType?: string;
}
/**
 * Vector bucket metadata
 * @property vectorBucketName - Unique name of the vector bucket
 * @property creationTime - Unix timestamp of when the bucket was created
 * @property encryptionConfiguration - Optional encryption settings
 */
interface VectorBucket {
  vectorBucketName: string;
  creationTime?: number;
  encryptionConfiguration?: EncryptionConfiguration;
}
/**
 * Metadata configuration for vector index
 * Defines which metadata keys should not be indexed for filtering
 * @property nonFilterableMetadataKeys - Array of metadata keys that cannot be used in filters
 */
interface MetadataConfiguration {
  nonFilterableMetadataKeys?: string[];
}
/**
 * Supported data types for vectors
 * Currently only float32 is supported
 */
type VectorDataType = 'float32' | (string & {});
/**
 * Distance metrics for vector similarity search
 */
type DistanceMetric = 'cosine' | 'euclidean' | 'dotproduct' | (string & {});
/**
 * Vector index configuration and metadata
 * @property indexName - Unique name of the index within the bucket
 * @property vectorBucketName - Name of the parent vector bucket
 * @property dataType - Data type of vector components (currently only 'float32')
 * @property dimension - Dimensionality of vectors (e.g., 384, 768, 1536)
 * @property distanceMetric - Similarity metric used for queries
 * @property metadataConfiguration - Configuration for metadata filtering
 * @property creationTime - Unix timestamp of when the index was created
 */
interface VectorIndex {
  indexName: string;
  vectorBucketName: string;
  dataType: VectorDataType;
  dimension: number;
  distanceMetric: DistanceMetric;
  metadataConfiguration?: MetadataConfiguration;
  creationTime?: number;
}
/**
 * Vector data representation
 * Vectors must be float32 arrays with dimensions matching the index
 * @property float32 - Array of 32-bit floating point numbers
 */
interface VectorData {
  float32: number[];
}
/**
 * Arbitrary JSON metadata attached to vectors
 * Keys configured as non-filterable in the index can be stored but not queried
 */
type VectorMetadata = Record<string, any>;
/**
 * Single vector object for insertion/update
 * @property key - Unique identifier for the vector
 * @property data - Vector embedding data
 * @property metadata - Optional arbitrary metadata
 */
interface VectorObject {
  key: string;
  data: VectorData;
  metadata?: VectorMetadata;
}
/**
 * Vector object returned from queries with optional distance
 * @property key - Unique identifier for the vector
 * @property data - Vector embedding data (if requested)
 * @property metadata - Arbitrary metadata (if requested)
 * @property distance - Similarity distance from query vector (if requested)
 */
interface VectorMatch {
  key: string;
  data?: VectorData;
  metadata?: VectorMetadata;
  distance?: number;
}
/**
 * Options for fetching vector buckets
 * @property prefix - Filter buckets by name prefix
 * @property maxResults - Maximum number of results to return (default: 100)
 * @property nextToken - Token for pagination from previous response
 */
interface ListVectorBucketsOptions {
  prefix?: string;
  maxResults?: number;
  nextToken?: string;
}
/**
 * Response from listing vector buckets
 * @property vectorBuckets - Array of bucket names
 * @property nextToken - Token for fetching next page (if more results exist)
 */
interface ListVectorBucketsResponse {
  vectorBuckets: {
    vectorBucketName: string;
  }[];
  nextToken?: string;
}
/**
 * Options for listing indexes within a bucket
 * @property vectorBucketName - Name of the parent vector bucket
 * @property prefix - Filter indexes by name prefix
 * @property maxResults - Maximum number of results to return (default: 100)
 * @property nextToken - Token for pagination from previous response
 */
interface ListIndexesOptions {
  vectorBucketName: string;
  prefix?: string;
  maxResults?: number;
  nextToken?: string;
}
/**
 * Response from listing indexes
 * @property indexes - Array of index names
 * @property nextToken - Token for fetching next page (if more results exist)
 */
interface ListIndexesResponse {
  indexes: {
    indexName: string;
  }[];
  nextToken?: string;
}
/**
 * Options for batch reading vectors
 * @property vectorBucketName - Name of the vector bucket
 * @property indexName - Name of the index
 * @property keys - Array of vector keys to retrieve
 * @property returnData - Whether to include vector data in response
 * @property returnMetadata - Whether to include metadata in response
 */
interface GetVectorsOptions {
  vectorBucketName: string;
  indexName: string;
  keys: string[];
  returnData?: boolean;
  returnMetadata?: boolean;
}
/**
 * Response from getting vectors
 * @property vectors - Array of retrieved vector objects
 */
interface GetVectorsResponse {
  vectors: VectorMatch[];
}
/**
 * Options for batch inserting/updating vectors
 * @property vectorBucketName - Name of the vector bucket
 * @property indexName - Name of the index
 * @property vectors - Array of vectors to insert/upsert (1-500 items)
 */
interface PutVectorsOptions {
  vectorBucketName: string;
  indexName: string;
  vectors: VectorObject[];
}
/**
 * Options for batch deleting vectors
 * @property vectorBucketName - Name of the vector bucket
 * @property indexName - Name of the index
 * @property keys - Array of vector keys to delete (1-500 items)
 */
interface DeleteVectorsOptions {
  vectorBucketName: string;
  indexName: string;
  keys: string[];
}
/**
 * Options for listing/scanning vectors in an index
 * Supports parallel scanning via segment configuration
 * @property vectorBucketName - Name of the vector bucket
 * @property indexName - Name of the index
 * @property maxResults - Maximum number of results to return (default: 500, max: 1000)
 * @property nextToken - Token for pagination from previous response
 * @property returnData - Whether to include vector data in response
 * @property returnMetadata - Whether to include metadata in response
 * @property segmentCount - Total number of parallel segments (1-16)
 * @property segmentIndex - Zero-based index of this segment (0 to segmentCount-1)
 */
interface ListVectorsOptions {
  vectorBucketName: string;
  indexName: string;
  maxResults?: number;
  nextToken?: string;
  returnData?: boolean;
  returnMetadata?: boolean;
  segmentCount?: number;
  segmentIndex?: number;
}
/**
 * Response from listing vectors
 * @property vectors - Array of vector objects
 * @property nextToken - Token for fetching next page (if more results exist)
 */
interface ListVectorsResponse {
  vectors: VectorMatch[];
  nextToken?: string;
}
/**
 * JSON filter expression for metadata filtering
 * Format and syntax depend on the S3 Vectors service implementation
 */
type VectorFilter = Record<string, any>;
/**
 * Options for querying similar vectors (ANN search)
 * @property vectorBucketName - Name of the vector bucket
 * @property indexName - Name of the index
 * @property queryVector - Query vector to find similar vectors
 * @property topK - Number of nearest neighbors to return (S3 vector buckets support 1-10,000; other backends may have a lower limit)
 * @property nextToken - S3 Vectors pagination token from a previous query response
 * @property filter - Optional JSON filter for metadata
 * @property returnDistance - Whether to include distance scores
 * @property returnMetadata - Whether to include metadata in results
 */
interface QueryVectorsOptions {
  vectorBucketName: string;
  indexName: string;
  queryVector: VectorData;
  topK: number;
  nextToken?: string;
  filter?: VectorFilter;
  returnDistance?: boolean;
  returnMetadata?: boolean;
}
/**
 * Response from vector similarity query
 * @property vectors - Array of similar vectors ordered by distance
 * @property distanceMetric - The distance metric used for the similarity search
 * @property nextToken - Token for fetching the next page of S3 Vectors results
 */
interface QueryVectorsResponse {
  vectors: VectorMatch[];
  distanceMetric?: DistanceMetric;
  nextToken?: string;
}
/**
 * Fetch-specific parameters like abort signals
 * @property signal - AbortSignal for cancelling requests
 */
interface VectorFetchParameters {
  signal?: AbortSignal;
}
/**
 * Standard response wrapper for successful operations
 * @property data - Response data of type T
 * @property error - Null on success
 */
interface SuccessResponse<T> {
  data: T;
  error: null;
}
/**
 * Standard response wrapper for failed operations
 * @property data - Null on error
 * @property error - StorageError with details (named StorageVectorsError for vector operations)
 */
interface ErrorResponse {
  data: null;
  error: StorageError;
}
/**
 * Union type for all API responses
 * Follows the pattern: { data: T, error: null } | { data: null, error: Error }
 */
type ApiResponse<T> = SuccessResponse<T> | ErrorResponse;
//#endregion
//#region src/lib/common/fetch.d.ts
type Fetch = typeof fetch;
//#endregion
//#region src/lib/common/BaseApiClient.d.ts
/**
 * @ignore
 * Base API client class for all Storage API classes
 * Provides common infrastructure for error handling and configuration
 *
 * @typeParam TError - The error type (StorageError or subclass)
 */
declare abstract class BaseApiClient<TError extends StorageError = StorageError> {
  protected url: string;
  protected headers: {
    [key: string]: string;
  };
  protected fetch: Fetch;
  protected shouldThrowOnError: boolean;
  protected namespace: ErrorNamespace;
  /**
   * Creates a new BaseApiClient instance
   * @param url - Base URL for API requests
   * @param headers - Default headers for API requests
   * @param fetch - Optional custom fetch implementation
   * @param namespace - Error namespace ('storage' or 'vectors')
   */
  constructor(url: string, headers?: {
    [key: string]: string;
  }, fetch?: Fetch, namespace?: ErrorNamespace);
  /**
   * Enable throwing errors instead of returning them.
   * When enabled, errors are thrown instead of returned in { data, error } format.
   *
   * @returns this - For method chaining
   */
  throwOnError(): this;
  /**
   * Set an HTTP header for the request.
   * Creates a shallow copy of headers to avoid mutating shared state.
   *
   * @param name - Header name
   * @param value - Header value
   * @returns this - For method chaining
   */
  setHeader(name: string, value: string): this;
  /**
   * Handles API operation with standardized error handling
   * Eliminates repetitive try-catch blocks across all API methods
   *
   * This wrapper:
   * 1. Executes the operation
   * 2. Returns { data, error: null } on success
   * 3. Returns { data: null, error } on failure (if shouldThrowOnError is false)
   * 4. Throws error on failure (if shouldThrowOnError is true)
   *
   * @typeParam T - The expected data type from the operation
   * @param operation - Async function that performs the API call
   * @returns Promise with { data, error } tuple
   *
   * @example Handling an operation
   * ```typescript
   * async listBuckets() {
   *   return this.handleOperation(async () => {
   *     return await get(this.fetch, `${this.url}/bucket`, {
   *       headers: this.headers,
   *     })
   *   })
   * }
   * ```
   */
  protected handleOperation<T>(operation: () => Promise<T>): Promise<{
    data: T;
    error: null;
  } | {
    data: null;
    error: TError;
  }>;
}
//#endregion
//#region src/packages/StreamDownloadBuilder.d.ts
declare class StreamDownloadBuilder implements Promise<DownloadResult<ReadableStream>> {
  private downloadFn;
  private shouldThrowOnError;
  readonly [Symbol.toStringTag]: string;
  private promise;
  constructor(downloadFn: () => Promise<Response>, shouldThrowOnError: boolean);
  then<TResult1 = DownloadResult<ReadableStream>, TResult2 = never>(onfulfilled?: ((value: DownloadResult<ReadableStream>) => TResult1 | PromiseLike<TResult1>) | null, onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | null): Promise<TResult1 | TResult2>;
  catch<TResult = never>(onrejected?: ((reason: any) => TResult | PromiseLike<TResult>) | null): Promise<DownloadResult<ReadableStream> | TResult>;
  finally(onfinally?: (() => void) | null): Promise<DownloadResult<ReadableStream>>;
  private getPromise;
  private execute;
}
//#endregion
//#region src/packages/BlobDownloadBuilder.d.ts
declare class BlobDownloadBuilder implements Promise<DownloadResult<Blob>> {
  private downloadFn;
  private shouldThrowOnError;
  readonly [Symbol.toStringTag]: string;
  private promise;
  constructor(downloadFn: () => Promise<Response>, shouldThrowOnError: boolean);
  asStream(): StreamDownloadBuilder;
  then<TResult1 = DownloadResult<Blob>, TResult2 = never>(onfulfilled?: ((value: DownloadResult<Blob>) => TResult1 | PromiseLike<TResult1>) | null, onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | null): Promise<TResult1 | TResult2>;
  catch<TResult = never>(onrejected?: ((reason: any) => TResult | PromiseLike<TResult>) | null): Promise<DownloadResult<Blob> | TResult>;
  finally(onfinally?: (() => void) | null): Promise<DownloadResult<Blob>>;
  private getPromise;
  private execute;
}
//#endregion
//#region src/packages/StorageFileApi.d.ts
type FileBody = ArrayBuffer | ArrayBufferView | Blob | Buffer | File | FormData | NodeJS.ReadableStream | ReadableStream<Uint8Array> | URLSearchParams | string;
declare class StorageFileApi extends BaseApiClient<StorageError> {
  protected bucketId: string | undefined;
  constructor(url: string, headers?: {
    [key: string]: string;
  }, bucketId?: string, fetch?: Fetch);
  /**
   * Uploads a file to an existing bucket or replaces an existing file at the specified path with a new one.
   *
   * @param method HTTP method.
   * @param path The relative file path. Should be of the format `folder/subfolder/filename.png`. The bucket must already exist before attempting to upload.
   * @param fileBody The body of the file to be stored in the bucket.
   */
  private uploadOrUpdate;
  /**
   * Uploads a file to an existing bucket.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param path The file path, including the file name. Should be of the format `folder/subfolder/filename.png`. The bucket must already exist before attempting to upload.
   * @param fileBody The body of the file to be stored in the bucket.
   * @param fileOptions Optional file upload options including cacheControl, contentType, upsert, and metadata.
   * @returns Promise with response containing file path, id, and fullPath or error
   *
   * @example Upload file
   * ```js
   * const avatarFile = event.target.files[0]
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .upload('public/avatar1.png', avatarFile, {
   *     cacheControl: '3600',
   *     upsert: false
   *   })
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "path": "public/avatar1.png",
   *     "fullPath": "avatars/public/avatar1.png"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @example Upload file using `ArrayBuffer` from base64 file data
   * ```js
   * import { decode } from 'base64-arraybuffer'
   *
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .upload('public/avatar1.png', decode('base64FileData'), {
   *     contentType: 'image/png'
   *   })
   * ```
   *
   * @example Handling errors
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .upload('public/avatar1.png', avatarFile)
   *
   * if (error) {
   *   // Log the full error so fields like `statusCode` and `error` (the
   *   // Storage error name, e.g. "Duplicate") aren't hidden behind `error.message`.
   *   console.error(error)
   *   return
   * }
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: none
   *   - `objects` table permissions: only `insert` when you are uploading new files and `select`, `insert` and `update` when you are upserting files
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   * - For React Native, using either `Blob`, `File` or `FormData` does not work as intended. Upload file using `ArrayBuffer` from base64 file data instead, see example below.
   */
  upload(path: string, fileBody: FileBody, fileOptions?: FileOptions): Promise<{
    data: {
      id: string;
      path: string;
      fullPath: string;
    };
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Upload a file with a token generated from `createSignedUploadUrl`.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param path The file path, including the file name. Should be of the format `folder/subfolder/filename.png`. The bucket must already exist before attempting to upload.
   * @param token The token generated from `createSignedUploadUrl`
   * @param fileBody The body of the file to be stored in the bucket.
   * @param fileOptions HTTP headers (cacheControl, contentType, etc.).
   * **Note:** The `upsert` option has no effect here. To enable upsert behavior,
   * pass `{ upsert: true }` when calling `createSignedUploadUrl()` instead.
   * @returns Promise with response containing file path and fullPath or error
   *
   * @example Upload to a signed URL
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .uploadToSignedUrl('folder/cat.jpg', 'token-from-createSignedUploadUrl', file)
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "path": "folder/cat.jpg",
   *     "fullPath": "avatars/folder/cat.jpg"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: none
   *   - `objects` table permissions: none
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  uploadToSignedUrl(path: string, token: string, fileBody: FileBody, fileOptions?: FileOptions): Promise<{
    data: null;
    error: StorageError;
  } | {
    data: {
      path: string;
      fullPath: any;
    };
    error: null;
  }>;
  /**
   * Creates a signed upload URL.
   * Signed upload URLs can be used to upload files to the bucket without further authentication.
   * They are valid for 2 hours.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param path The file path, including the current file name. For example `folder/image.png`.
   * @param options.upsert If set to true, allows the file to be overwritten if it already exists.
   * @returns Promise with response containing signed upload URL, token, and path or error
   *
   * @example Create Signed Upload URL
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .createSignedUploadUrl('folder/cat.jpg')
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "signedUrl": "https://example.supabase.co/storage/v1/object/upload/sign/avatars/folder/cat.jpg?token=<TOKEN>",
   *     "path": "folder/cat.jpg",
   *     "token": "<TOKEN>"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: none
   *   - `objects` table permissions: `insert`
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  createSignedUploadUrl(path: string, options?: {
    upsert: boolean;
  }): Promise<{
    data: {
      signedUrl: string;
      token: string;
      path: string;
    };
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Replaces an existing file at the specified path with a new one.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param path The relative file path. Should be of the format `folder/subfolder/filename.png`. The bucket must already exist before attempting to update.
   * @param fileBody The body of the file to be stored in the bucket.
   * @param fileOptions Optional file upload options including cacheControl, contentType, and metadata.
   * **Note:** The `upsert` option has no effect here. `update()` always replaces the
   * file at the given path, so the `x-upsert` header is not sent. To control upsert
   * behavior, use `upload()` instead.
   * @returns Promise with response containing file path, id, and fullPath or error
   *
   * @example Update file
   * ```js
   * const avatarFile = event.target.files[0]
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .update('public/avatar1.png', avatarFile, {
   *     cacheControl: '3600'
   *   })
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "path": "public/avatar1.png",
   *     "fullPath": "avatars/public/avatar1.png"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @example Update file using `ArrayBuffer` from base64 file data
   * ```js
   * import {decode} from 'base64-arraybuffer'
   *
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .update('public/avatar1.png', decode('base64FileData'), {
   *     contentType: 'image/png'
   *   })
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: none
   *   - `objects` table permissions: `update` and `select`
   * - `update()` always replaces the file at the given path regardless of the `upsert` option.
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   * - For React Native, using either `Blob`, `File` or `FormData` does not work as intended. Update file using `ArrayBuffer` from base64 file data instead, see example below.
   */
  update(path: string, fileBody: ArrayBuffer | ArrayBufferView | Blob | Buffer | File | FormData | NodeJS.ReadableStream | ReadableStream<Uint8Array> | URLSearchParams | string, fileOptions?: FileOptions): Promise<{
    data: {
      id: string;
      path: string;
      fullPath: string;
    };
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Moves an existing file to a new path in the same bucket.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param fromPath The original file path, including the current file name. For example `folder/image.png`.
   * @param toPath The new file path, including the new file name. For example `folder/image-new.png`.
   * @param options The destination options.
   * @param options.sourceVersionId The version id of the source object to move.
   * @returns Promise with response containing success message or error
   *
   * @example Move file
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .move('public/avatar1.png', 'private/avatar2.png')
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "message": "Successfully moved"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: none
   *   - `objects` table permissions: `update` and `select`
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  move(fromPath: string, toPath: string, options?: DestinationOptions): Promise<{
    data: {
      message: string;
    };
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Copies an existing file to a new path in the same bucket.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param fromPath The original file path, including the current file name. For example `folder/image.png`.
   * @param toPath The new file path, including the new file name. For example `folder/image-copy.png`.
   * @param options The destination options.
   * @param options.sourceVersionId The version id of the source object to copy.
   * @returns Promise with response containing copied file path or error
   *
   * @example Copy file
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .copy('public/avatar1.png', 'private/avatar2.png')
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "path": "avatars/private/avatar2.png"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: none
   *   - `objects` table permissions: `insert` and `select`
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  copy(fromPath: string, toPath: string, options?: DestinationOptions): Promise<{
    data: {
      path: string;
    };
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Creates a signed URL. Use a signed URL to share a file for a fixed amount of time.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param path The file path, including the current file name. For example `folder/image.png`.
   * @param expiresIn The number of seconds until the signed URL expires. For example, `60` for a URL which is valid for one minute.
   * @param options.download triggers the file as a download if set to true. Set this parameter as the name of the file if you want to trigger the download with a different filename.
   * @param options.transform Transform the asset before serving it to the client.
   * @param options.cacheNonce Append a cache nonce parameter to the URL to invalidate the cache.
   * @param options.versionId Create a signed URL for a specific object version rather than the current one.
   * @returns Promise with response containing signed URL or error
   *
   * @example Create Signed URL
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .createSignedUrl('folder/avatar1.png', 60)
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "signedUrl": "https://example.supabase.co/storage/v1/object/sign/avatars/folder/avatar1.png?token=<TOKEN>"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @example Create a signed URL for an asset with transformations
   * ```js
   * const { data } = await supabase
   *   .storage
   *   .from('avatars')
   *   .createSignedUrl('folder/avatar1.png', 60, {
   *     transform: {
   *       width: 100,
   *       height: 100,
   *     }
   *   })
   * ```
   *
   * @example Create a signed URL which triggers the download of the asset
   * ```js
   * const { data } = await supabase
   *   .storage
   *   .from('avatars')
   *   .createSignedUrl('folder/avatar1.png', 60, {
   *     download: true,
   *   })
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: none
   *   - `objects` table permissions: `select`
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  createSignedUrl(path: string, expiresIn: number, options?: {
    download?: string | boolean;
    transform?: TransformOptions;
    cacheNonce?: string;
    versionId?: string;
  }): Promise<{
    data: {
      signedUrl: string;
    };
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Creates multiple signed URLs. Use a signed URL to share a file for a fixed amount of time.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param paths The file paths to be downloaded, including the current file names. For example `['folder/image.png', 'folder2/image2.png']`.
   * @param expiresIn The number of seconds until the signed URLs expire. For example, `60` for URLs which are valid for one minute.
   * @param options.download triggers the file as a download if set to true. Set this parameter as the name of the file if you want to trigger the download with a different filename.
   * @param options.cacheNonce Append a cache nonce parameter to the URL to invalidate the cache.
   * @returns Promise with response containing array of objects with signedUrl, path, and error or error
   *
   * @example Create Signed URLs
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .createSignedUrls(['folder/avatar1.png', 'folder/avatar2.png'], 60)
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": [
   *     {
   *       "error": null,
   *       "path": "folder/avatar1.png",
   *       "signedURL": "/object/sign/avatars/folder/avatar1.png?token=<TOKEN>",
   *       "signedUrl": "https://example.supabase.co/storage/v1/object/sign/avatars/folder/avatar1.png?token=<TOKEN>"
   *     },
   *     {
   *       "error": null,
   *       "path": "folder/avatar2.png",
   *       "signedURL": "/object/sign/avatars/folder/avatar2.png?token=<TOKEN>",
   *       "signedUrl": "https://example.supabase.co/storage/v1/object/sign/avatars/folder/avatar2.png?token=<TOKEN>"
   *     }
   *   ],
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: none
   *   - `objects` table permissions: `select`
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  createSignedUrls(paths: string[], expiresIn: number, options?: {
    download?: string | boolean;
    cacheNonce?: string;
  }): Promise<{
    data: {
      error: string | null;
      path: string | null;
      signedURL: string | null;
      signedUrl: string | null;
    }[];
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Downloads a file from a private bucket. For public buckets, make a request to the URL returned from `getPublicUrl` instead.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param path The full path and file name of the file to be downloaded. For example `folder/image.png`.
   * @param options Optional settings: `transform` to transform the asset before serving it to the client, `cacheNonce` to append a cache nonce parameter to the URL to invalidate the cache, and `versionId` to download a specific object version.
   * @param parameters Additional fetch parameters like signal for cancellation. Supports standard fetch options including cache control.
   * @returns BlobDownloadBuilder instance for downloading the file
   *
   * @example Download file
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .download('folder/avatar1.png')
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": <BLOB>,
   *   "error": null
   * }
   * ```
   *
   * @example Download file with transformations
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .download('folder/avatar1.png', {
   *     transform: {
   *       width: 100,
   *       height: 100,
   *       quality: 80
   *     }
   *   })
   * ```
   *
   * @example Download with cache control (useful in Edge Functions)
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .download('folder/avatar1.png', {}, { cache: 'no-store' })
   * ```
   *
   * @example Download with abort signal
   * ```js
   * const controller = new AbortController()
   * setTimeout(() => controller.abort(), 5000)
   *
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .download('folder/avatar1.png', {}, { signal: controller.signal })
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: none
   *   - `objects` table permissions: `select`
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  download<Options extends {
    transform?: TransformOptions;
    cacheNonce?: string;
    versionId?: string;
  }>(path: string, options?: Options, parameters?: FetchParameters): BlobDownloadBuilder;
  /**
   * Retrieves the details of an existing file.
   *
   * Returns detailed file metadata including size, content type, and timestamps.
   * Note: The API returns `last_modified` field, not `updated_at`.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param path The file path, including the file name. For example `folder/image.png`.
   * @param options Optional settings, including `versionId` to retrieve a specific object version.
   * @returns Promise with response containing file metadata or error
   *
   * @example Get file info
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .info('folder/avatar1.png')
   *
   * if (data) {
   *   console.log('Last modified:', data.lastModified)
   *   console.log('Size:', data.size)
   * }
   * ```
   */
  info(path: string, options?: {
    versionId?: string;
  }): Promise<{
    data: Camelize<FileObjectV2>;
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Checks the existence of a file.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param path The file path, including the file name. For example `folder/image.png`.
   * @returns Promise with response containing boolean indicating file existence or error
   *
   * @example Check file existence
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .exists('folder/avatar1.png')
   * ```
   */
  exists(path: string): Promise<{
    data: boolean;
    error: null;
  } | {
    data: boolean;
    error: StorageError;
  }>;
  /**
   * A simple convenience function to get the URL for an asset in a public bucket. If you do not want to use this function, you can construct the public URL by concatenating the bucket URL with the path to the asset.
   * This function does not verify if the bucket is public. If a public URL is created for a bucket which is not public, you will not be able to download the asset.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param path The path and name of the file to generate the public URL for. For example `folder/image.png`.
   * @param options.download Triggers the file as a download if set to true. Set this parameter as the name of the file if you want to trigger the download with a different filename.
   * @param options.transform Transform the asset before serving it to the client.
   * @param options.cacheNonce Append a cache nonce parameter to the URL to invalidate the cache.
   * @param options.versionId Return the URL for a specific object version rather than the current one.
   * @returns Object with public URL
   *
   * @example Returns the URL for an asset in a public bucket
   * ```js
   * const { data } = supabase
   *   .storage
   *   .from('public-bucket')
   *   .getPublicUrl('folder/avatar1.png')
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "publicUrl": "https://example.supabase.co/storage/v1/object/public/public-bucket/folder/avatar1.png"
   *   }
   * }
   * ```
   *
   * @example Returns the URL for an asset in a public bucket with transformations
   * ```js
   * const { data } = supabase
   *   .storage
   *   .from('public-bucket')
   *   .getPublicUrl('folder/avatar1.png', {
   *     transform: {
   *       width: 100,
   *       height: 100,
   *     }
   *   })
   * ```
   *
   * @example Returns the URL which triggers the download of an asset in a public bucket
   * ```js
   * const { data } = supabase
   *   .storage
   *   .from('public-bucket')
   *   .getPublicUrl('folder/avatar1.png', {
   *     download: true,
   *   })
   * ```
   *
   * @remarks
   * - The bucket needs to be set to public, either via [updateBucket()](/docs/reference/javascript/storage-updatebucket) or by going to Storage on [supabase.com/dashboard](https://supabase.com/dashboard), clicking the overflow menu on a bucket and choosing "Make public"
   * - RLS policy permissions required:
   *   - `buckets` table permissions: none
   *   - `objects` table permissions: none
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  getPublicUrl(path: string, options?: {
    download?: string | boolean;
    transform?: TransformOptions;
    cacheNonce?: string;
    versionId?: string;
  }): {
    data: {
      publicUrl: string;
    };
  };
  /**
   * Deletes files within the same bucket
   *
   * Returns an array of FileObject entries for the deleted files. Note that deprecated
   * fields like `bucket_id` may or may not be present in the response - do not rely on them.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param paths An array of files to delete. Each entry is either a path (deletes whichever
   * version is currently at that path, e.g. `'folder/image.png'`), or `{ path, versionId }` to
   * delete an exact version current or archived (e.g. `{ path: 'folder/image.png', versionId: '...' }`).
   * @returns Promise with response containing array of deleted file objects or error
   *
   * @example Delete file
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .remove(['folder/avatar1.png'])
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": [],
   *   "error": null
   * }
   * ```
   *
   * @example Delete a specific object version
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .remove([{ path: 'folder/avatar1.png', versionId: 'noncurrent-version-id' }])
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: none
   *   - `objects` table permissions: `delete` and `select`
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  remove(paths: DeleteObjectEntry[]): Promise<{
    data: FileObject[];
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Purges the CDN cache for a single object in this bucket.
   *
   * Maps to `DELETE /cdn/{bucket}/{path}` on the Storage API. The server
   * issues a CDN invalidation for the object and returns `{ message: 'success' }`.
   *
   * **Requires the `service_role` key.** The underlying endpoint enforces
   * `service_role` JWT — calls made with the anon key or a user JWT will be
   * rejected by the server.
   *
   * **Hosted CDN feature.** On self-hosted Supabase, the Storage service must
   * have `CDN_PURGE_ENDPOINT_URL` configured and the `purgeCache` tenant
   * feature enabled, otherwise the server returns an error.
   *
   * Operates on a single object path. There is no wildcard or recursion: pass
   * the exact path of the object you want invalidated.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param path The path (relative to the bucket) of the object to purge, e.g. `folder/avatar.png`.
   * @param options Optional purge cache options.
   * @param options.transformations If true, purges only transformations (resized/formatted variants), leaving the original cached file intact.
   * @param parameters Optional fetch parameters such as an `AbortController` signal.
   * @returns Promise with `{ data: { message }, error: null }` on success or `{ data: null, error }` on failure.
   *
   * @example Purge a single cached object
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .purgeCache('folder/avatar1.png')
   * ```
   *
   * @example Purge only transformations for a single object
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .purgeCache('folder/avatar1.png', { transformations: true })
   * ```
   */
  purgeCache(path: string, options?: PurgeCacheOptions, parameters?: FetchParameters): Promise<{
    data: {
      message: string;
    };
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Get file metadata
   * @param id the file id to retrieve metadata
   */
  /**
   * Update file metadata
   * @param id the file id to update metadata
   * @param meta the new file metadata
   */
  /**
   * Lists all the files and folders within a path of the bucket.
   *
   * **Important:** For folder entries, fields like `id`, `updated_at`, `created_at`,
   * `last_accessed_at`, and `metadata` will be `null`. Only files have these fields populated.
   * Additionally, deprecated fields like `bucket_id`, `owner`, and `buckets` are NOT returned
   * by this method.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param path The folder path.
   * @param options Search options including limit (defaults to 100), offset, sortBy, and search
   * @param parameters Optional fetch parameters including signal for cancellation
   * @returns Promise with response containing array of files/folders or error
   *
   * @example List files in a bucket
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .list('folder', {
   *     limit: 100,
   *     offset: 0,
   *     sortBy: { column: 'name', order: 'asc' },
   *   })
   *
   * // Handle files vs folders
   * data?.forEach(item => {
   *   if (item.id !== null) {
   *     // It's a file
   *     console.log('File:', item.name, 'Size:', item.metadata?.size)
   *   } else {
   *     // It's a folder
   *     console.log('Folder:', item.name)
   *   }
   * })
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": [
   *     {
   *       "name": "avatar1.png",
   *       "id": "e668cf7f-821b-4a2f-9dce-7dfa5dd1cfd2",
   *       "updated_at": "2024-05-22T23:06:05.580Z",
   *       "created_at": "2024-05-22T23:04:34.443Z",
   *       "last_accessed_at": "2024-05-22T23:04:34.443Z",
   *       "metadata": {
   *         "eTag": "\"c5e8c553235d9af30ef4f6e280790b92\"",
   *         "size": 32175,
   *         "mimetype": "image/png",
   *         "cacheControl": "max-age=3600",
   *         "lastModified": "2024-05-22T23:06:05.574Z",
   *         "contentLength": 32175,
   *         "httpStatusCode": 200
   *       }
   *     }
   *   ],
   *   "error": null
   * }
   * ```
   *
   * @example Search files in a bucket
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .list('folder', {
   *     limit: 100,
   *     offset: 0,
   *     sortBy: { column: 'name', order: 'asc' },
   *     search: 'jon'
   *   })
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: none
   *   - `objects` table permissions: `select`
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  list(path?: string, options?: SearchOptions, parameters?: FetchParameters): Promise<{
    data: FileObject[];
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Lists all the files and folders within a bucket using the V2 API with pagination support.
   *
   * **Important:** Folder entries in the `folders` array only contain `name` and optionally `key` —
   * they have no `id`, timestamps, or `metadata` fields. Full file metadata is only available
   * on entries in the `objects` array.
   *
   * @experimental this method signature might change in the future
   *
   * @category Storage
   * @subcategory File Buckets
   * @param options Search options including prefix, cursor for pagination, limit, with_delimiter
   * @param parameters Optional fetch parameters including signal for cancellation
   * @returns Promise with response containing folders/objects arrays with pagination info or error
   *
   * @example List files with pagination
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .from('avatars')
   *   .listV2({
   *     prefix: 'folder/',
   *     limit: 100,
   *   })
   *
   * // Handle pagination
   * if (data?.hasNext) {
   *   const nextPage = await supabase
   *     .storage
   *     .from('avatars')
   *     .listV2({
   *       prefix: 'folder/',
   *       cursor: data.nextCursor,
   *     })
   * }
   *
   * // Handle files vs folders
   * data?.objects.forEach(file => {
   *   if (file.id !== null) {
   *     console.log('File:', file.name, 'Size:', file.metadata?.size)
   *   }
   * })
   * data?.folders.forEach(folder => {
   *   console.log('Folder:', folder.name)
   * })
   * ```
   */
  listV2(options?: SearchV2Options, parameters?: FetchParameters): Promise<{
    data: SearchV2Result;
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  protected encodeMetadata(metadata: Record<string, any>): string;
  toBase64(data: string): string;
  private _getFinalPath;
  private _removeEmptyFolders;
  /** Modifies the `query`, appending values the from `transform` */
  private applyTransformOptsToQuery;
}
//#endregion
//#region src/packages/StorageBucketApi.d.ts
declare class StorageBucketApi extends BaseApiClient<StorageError> {
  constructor(url: string, headers?: {
    [key: string]: string;
  }, fetch?: Fetch, opts?: StorageClientOptions);
  /**
   * Retrieves the details of all Storage buckets within an existing project.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param options Query parameters for listing buckets
   * @param options.limit Maximum number of buckets to return
   * @param options.offset Number of buckets to skip
   * @param options.sortColumn Column to sort by ('id', 'name', 'created_at', 'updated_at')
   * @param options.sortOrder Sort order ('asc' or 'desc')
   * @param options.search Search term to filter bucket names
   * @returns Promise with response containing array of buckets or error
   *
   * @example List buckets
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .listBuckets()
   * ```
   *
   * @example List buckets with options
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .listBuckets({
   *     limit: 10,
   *     offset: 0,
   *     sortColumn: 'created_at',
   *     sortOrder: 'desc',
   *     search: 'prod'
   *   })
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: `select`
   *   - `objects` table permissions: none
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  listBuckets(options?: ListBucketOptions): Promise<{
    data: Bucket[];
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Retrieves the details of an existing Storage bucket.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param id The unique identifier of the bucket you would like to retrieve.
   * @returns Promise with response containing bucket details or error
   *
   * @example Get bucket
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .getBucket('avatars')
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "id": "avatars",
   *     "name": "avatars",
   *     "owner": "",
   *     "public": false,
   *     "file_size_limit": 1024,
   *     "allowed_mime_types": [
   *       "image/png"
   *     ],
   *     "created_at": "2024-05-22T22:26:05.100Z",
   *     "updated_at": "2024-05-22T22:26:05.100Z"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: `select`
   *   - `objects` table permissions: none
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  getBucket(id: string): Promise<{
    data: Bucket;
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Creates a new Storage bucket
   *
   * @category Storage
   * @subcategory File Buckets
   * @param id A unique identifier for the bucket you are creating.
   * @param options.public The visibility of the bucket. Public buckets don't require an authorization token to download objects, but still require a valid token for all other operations. By default, buckets are private.
   * @param options.fileSizeLimit specifies the max file size in bytes that can be uploaded to this bucket.
   * The global file size limit takes precedence over this value.
   * The default value is null, which doesn't set a per bucket file size limit.
   * @param options.allowedMimeTypes specifies the allowed mime types that this bucket can accept during upload.
   * The default value is null, which allows files with all mime types to be uploaded.
   * Each mime type specified can be a wildcard, e.g. image/*, or a specific mime type, e.g. image/png.
   * @param options.type (private-beta) specifies the bucket type. see `BucketType` for more details.
   *   - default bucket type is `STANDARD`
   * @param options.versioningStatus the bucket's initial object versioning status.
   * The default value is `DISABLED`
   * @returns Promise with response containing newly created bucket name or error
   *
   * @example Create bucket
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .createBucket('avatars', {
   *     public: false,
   *     allowedMimeTypes: ['image/png'],
   *     fileSizeLimit: 1024
   *   })
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "name": "avatars"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: `insert`
   *   - `objects` table permissions: none
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  createBucket(id: string, options?: {
    public: boolean;
    fileSizeLimit?: number | string | null;
    allowedMimeTypes?: string[] | null;
    type?: BucketType;
    versioningStatus?: CreateSettableVersioningStatus;
  }): Promise<{
    data: Pick<Bucket, 'name'>;
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Updates a Storage bucket
   *
   * @category Storage
   * @subcategory File Buckets
   * @param id A unique identifier for the bucket you are updating.
   * @param options.public The visibility of the bucket. Public buckets don't require an authorization token to download objects, but still require a valid token for all other operations.
   * @param options.fileSizeLimit specifies the max file size in bytes that can be uploaded to this bucket.
   * The global file size limit takes precedence over this value.
   * The default value is null, which doesn't set a per bucket file size limit.
   * @param options.allowedMimeTypes specifies the allowed mime types that this bucket can accept during upload.
   * The default value is null, which allows files with all mime types to be uploaded.
   * Each mime type specified can be a wildcard, e.g. image/*, or a specific mime type, e.g. image/png.
   * @param options.versioningStatus the bucket's new object versioning status. `DISABLED` is not
   * valid here, there's no transition back to it once versioning has been touched.
   * @returns Promise with response containing success message or error
   *
   * @example Update bucket
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .updateBucket('avatars', {
   *     public: false,
   *     allowedMimeTypes: ['image/png'],
   *     fileSizeLimit: 1024
   *   })
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "message": "Successfully updated"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: `select` and `update`
   *   - `objects` table permissions: none
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  updateBucket(id: string, options: {
    public: boolean;
    fileSizeLimit?: number | string | null;
    allowedMimeTypes?: string[] | null;
    versioningStatus?: UpdateSettableVersioningStatus;
  }): Promise<{
    data: {
      message: string;
    };
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Removes all objects inside a single bucket.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param id The unique identifier of the bucket you would like to empty.
   * @returns Promise with success message or error
   *
   * @example Empty bucket
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .emptyBucket('avatars')
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "message": "Successfully emptied"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: `select`
   *   - `objects` table permissions: `select` and `delete`
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  emptyBucket(id: string): Promise<{
    data: {
      message: string;
    };
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Deletes an existing bucket. A bucket can't be deleted with existing objects inside it.
   * You must first `empty()` the bucket.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param id The unique identifier of the bucket you would like to delete.
   * @returns Promise with success message or error
   *
   * @example Delete bucket
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .deleteBucket('avatars')
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "message": "Successfully deleted"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: `select` and `delete`
   *   - `objects` table permissions: none
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  deleteBucket(id: string): Promise<{
    data: {
      message: string;
    };
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Returns the lifecycle policy stored on a bucket.
   *
   * Fails with `NoSuchLifecycleConfiguration` when the bucket has no policy.
   *
   * These rules expire previous versions of objects, not the current one.
   * Turn versioning on or there is nothing for the policy to act on.
   * Standard buckets only. Returns `FeatureNotEnabled` if lifecycle is off
   * for the project.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param id The unique identifier of the bucket.
   * @returns Promise with the lifecycle configuration or error
   *
   * @example Get lifecycle configuration
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .getBucketLifecycle('avatars')
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "rules": [
   *       {
   *         "id": "expire-history",
   *         "status": "Enabled",
   *         "filter": {},
   *         "noncurrentVersionExpiration": {
   *           "noncurrentDays": 30,
   *           "newerNoncurrentVersions": 2
   *         }
   *       }
   *     ]
   *   },
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: `select`
   *   - `objects` table permissions: none
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  getBucketLifecycle(id: string): Promise<{
    data: BucketLifecycleConfiguration;
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Replaces the lifecycle policy on a bucket.
   *
   * The `rules` array you send is the whole policy. Anything previously stored
   * is overwritten. Send at least one rule. Call {@link deleteBucketLifecycle}
   * to remove the policy.
   *
   * Each rule currently supports only `noncurrentVersionExpiration`. `filter`
   * is required and must be `{}`. Prefix filters, tag filters, and current-object
   * expiration are rejected. Rule IDs must be unique. Omit `id` and the
   * server generates one.
   *
   * Standard buckets only. Returns `FeatureNotEnabled` if lifecycle is off
   * for the project.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param id The unique identifier of the bucket.
   * @param configuration The full lifecycle configuration to store.
   * @returns Promise with the stored configuration or error
   *
   * @example Replace lifecycle configuration
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .updateBucketLifecycle('avatars', {
   *     rules: [
   *       {
   *         id: 'expire-history',
   *         status: 'Enabled',
   *         filter: {},
   *         noncurrentVersionExpiration: {
   *           noncurrentDays: 30,
   *           newerNoncurrentVersions: 2,
   *         },
   *       },
   *     ],
   *   })
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: `select` and `update`
   *   - `objects` table permissions: none
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  updateBucketLifecycle(id: string, configuration: BucketLifecycleConfiguration): Promise<{
    data: BucketLifecycleConfiguration;
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Removes the lifecycle policy from a bucket.
   *
   * Safe to call when no policy is stored. The response is still success.
   * Standard buckets only. Returns `FeatureNotEnabled` if lifecycle is off
   * for the project.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param id The unique identifier of the bucket.
   * @returns Promise with success message or error
   *
   * @example Delete lifecycle configuration
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .deleteBucketLifecycle('avatars')
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "message": "Successfully deleted"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - RLS policy permissions required:
   *   - `buckets` table permissions: `select` and `update`
   *   - `objects` table permissions: none
   * - Refer to the [Storage guide](/docs/guides/storage/security/access-control) on how access control works
   */
  deleteBucketLifecycle(id: string): Promise<{
    data: {
      message: string;
    };
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * Purges the CDN cache for an entire bucket.
   *
   * Maps to `DELETE /cdn/{bucket}` on the Storage API. The server
   * issues a CDN invalidation for the bucket and returns `{ message: 'success' }`.
   *
   * **Requires the `service_role` key.** The underlying endpoint enforces
   * `service_role` JWT — calls made with the anon key or a user JWT will be
   * rejected by the server.
   *
   * **Hosted CDN feature.** On self-hosted Supabase, the Storage service must
   * have `CDN_PURGE_ENDPOINT_URL` configured and the `purgeCache` tenant
   * feature enabled, otherwise the server returns an error.
   *
   * @category Storage
   * @subcategory File Buckets
   * @param id The unique identifier of the bucket you would like to purge from cache.
   * @param options Optional purge cache options.
   * @param options.transformations If true, purges only transformations (resized/formatted variants), leaving original cached files intact.
   * @param parameters Optional fetch parameters such as an `AbortController` signal.
   * @returns Promise with `{ data: { message }, error: null }` on success or `{ data: null, error }` on failure.
   *
   * @example Purge cache for an entire bucket
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .purgeBucketCache('avatars')
   * ```
   *
   * @example Purge only transformations for an entire bucket
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .purgeBucketCache('avatars', { transformations: true })
   * ```
   */
  purgeBucketCache(id: string, options?: PurgeCacheOptions, parameters?: FetchParameters): Promise<{
    data: {
      message: string;
    };
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  private bucketLifecycleUrl;
  private listBucketOptionsToQueryString;
}
//#endregion
//#region src/packages/StorageAnalyticsClient.d.ts
type WrapAsyncMethod<T> = T extends ((...args: infer A) => Promise<infer R>) ? (...args: A) => Promise<{
  data: R;
  error: null;
} | {
  data: null;
  error: IcebergError;
}> : T;
type WrappedIcebergRestCatalog = { [K in keyof IcebergRestCatalog]: WrapAsyncMethod<IcebergRestCatalog[K]> };
/**
 * Client class for managing Analytics Buckets using Iceberg tables
 * Provides methods for creating, listing, and deleting analytics buckets
 */
declare class StorageAnalyticsClient extends BaseApiClient<StorageError> {
  /**
   * @alpha
   *
   * Creates a new StorageAnalyticsClient instance
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Analytics Buckets
   * @param url - The base URL for the storage API
   * @param headers - HTTP headers to include in requests
   * @param fetch - Optional custom fetch implementation
   *
   * @example Using supabase-js (recommended)
   * ```typescript
   * import { createClient } from '@supabase/supabase-js'
   *
   * const supabase = createClient('https://xyzcompany.supabase.co', 'your-publishable-key')
   * const { data, error } = await supabase.storage.analytics.listBuckets()
   * ```
   *
   * @example Standalone import for bundle-sensitive environments
   * ```typescript
   * import { StorageAnalyticsClient } from '@supabase/storage-js'
   *
   * const client = new StorageAnalyticsClient(url, headers)
   * ```
   */
  constructor(url: string, headers?: {
    [key: string]: string;
  }, fetch?: Fetch);
  /**
   * @alpha
   *
   * Creates a new analytics bucket using Iceberg tables
   * Analytics buckets are optimized for analytical queries and data processing
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Analytics Buckets
   * @param name A unique name for the bucket you are creating
   * @returns Promise with response containing newly created analytics bucket or error
   *
   * @example Create analytics bucket
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .analytics
   *   .createBucket('analytics-data')
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "name": "analytics-data",
   *     "type": "ANALYTICS",
   *     "format": "iceberg",
   *     "created_at": "2024-05-22T22:26:05.100Z",
   *     "updated_at": "2024-05-22T22:26:05.100Z"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - Creates a new analytics bucket using Iceberg tables
   * - Analytics buckets are optimized for analytical queries and data processing
   */
  createBucket(name: string): Promise<{
    data: AnalyticBucket;
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * @alpha
   *
   * Retrieves the details of all Analytics Storage buckets within an existing project
   * Only returns buckets of type 'ANALYTICS'
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Analytics Buckets
   * @param options Query parameters for listing buckets
   * @param options.limit Maximum number of buckets to return
   * @param options.offset Number of buckets to skip
   * @param options.sortColumn Column to sort by ('name', 'created_at', 'updated_at')
   * @param options.sortOrder Sort order ('asc' or 'desc')
   * @param options.search Search term to filter bucket names
   * @returns Promise with response containing array of analytics buckets or error
   *
   * @example List analytics buckets
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .analytics
   *   .listBuckets({
   *     limit: 10,
   *     offset: 0,
   *     sortColumn: 'created_at',
   *     sortOrder: 'desc'
   *   })
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": [
   *     {
   *       "name": "analytics-data",
   *       "type": "ANALYTICS",
   *       "format": "iceberg",
   *       "created_at": "2024-05-22T22:26:05.100Z",
   *       "updated_at": "2024-05-22T22:26:05.100Z"
   *     }
   *   ],
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - Retrieves the details of all Analytics Storage buckets within an existing project
   * - Only returns buckets of type 'ANALYTICS'
   */
  listBuckets(options?: {
    limit?: number;
    offset?: number;
    sortColumn?: 'name' | 'created_at' | 'updated_at';
    sortOrder?: 'asc' | 'desc';
    search?: string;
  }): Promise<{
    data: AnalyticBucket[];
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * @alpha
   *
   * Deletes an existing analytics bucket
   * A bucket can't be deleted with existing objects inside it
   * You must first empty the bucket before deletion
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Analytics Buckets
   * @param bucketName The unique identifier of the bucket you would like to delete
   * @returns Promise with response containing success message or error
   *
   * @example Delete analytics bucket
   * ```js
   * const { data, error } = await supabase
   *   .storage
   *   .analytics
   *   .deleteBucket('analytics-data')
   * ```
   *
   * Response:
   * ```json
   * {
   *   "data": {
   *     "message": "Successfully deleted"
   *   },
   *   "error": null
   * }
   * ```
   *
   * @remarks
   * - Deletes an analytics bucket
   */
  deleteBucket(bucketName: string): Promise<{
    data: {
      message: string;
    };
    error: null;
  } | {
    data: null;
    error: StorageError;
  }>;
  /**
   * @alpha
   *
   * Get an Iceberg REST Catalog client configured for a specific analytics bucket
   * Use this to perform advanced table and namespace operations within the bucket
   * The returned client provides full access to the Apache Iceberg REST Catalog API
   * with the Supabase `{ data, error }` pattern for consistent error handling on all operations.
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Analytics Buckets
   * @param bucketName - The name of the analytics bucket (warehouse) to connect to
   * @returns The wrapped Iceberg catalog client
   * @throws {StorageError} If the bucket name is invalid
   *
   * @example Get catalog and create table
   * ```js
   * // First, create an analytics bucket
   * const { data: bucket, error: bucketError } = await supabase
   *   .storage
   *   .analytics
   *   .createBucket('analytics-data')
   *
   * // Get the Iceberg catalog for that bucket
   * const catalog = supabase.storage.analytics.from('analytics-data')
   *
   * // Create a namespace
   * const { error: nsError } = await catalog.createNamespace({ namespace: ['default'] })
   *
   * // Create a table with schema
   * const { data: tableMetadata, error: tableError } = await catalog.createTable(
   *   { namespace: ['default'] },
   *   {
   *     name: 'events',
   *     schema: {
   *       type: 'struct',
   *       fields: [
   *         { id: 1, name: 'id', type: 'long', required: true },
   *         { id: 2, name: 'timestamp', type: 'timestamp', required: true },
   *         { id: 3, name: 'user_id', type: 'string', required: false }
   *       ],
   *       'schema-id': 0,
   *       'identifier-field-ids': [1]
   *     },
   *     'partition-spec': {
   *       'spec-id': 0,
   *       fields: []
   *     },
   *     'write-order': {
   *       'order-id': 0,
   *       fields: []
   *     },
   *     properties: {
   *       'write.format.default': 'parquet'
   *     }
   *   }
   * )
   * ```
   *
   * @example List tables in namespace
   * ```js
   * const catalog = supabase.storage.analytics.from('analytics-data')
   *
   * // List all tables in the default namespace
   * const { data: tables, error: listError } = await catalog.listTables({ namespace: ['default'] })
   * if (listError) {
   *   if (listError.isNotFound()) {
   *     console.log('Namespace not found')
   *   }
   *   return
   * }
   * console.log(tables) // [{ namespace: ['default'], name: 'events' }]
   * ```
   *
   * @example Working with namespaces
   * ```js
   * const catalog = supabase.storage.analytics.from('analytics-data')
   *
   * // List all namespaces
   * const { data: namespaces } = await catalog.listNamespaces()
   *
   * // Create namespace with properties
   * await catalog.createNamespace(
   *   { namespace: ['production'] },
   *   { properties: { owner: 'data-team', env: 'prod' } }
   * )
   * ```
   *
   * @example Cleanup operations
   * ```js
   * const catalog = supabase.storage.analytics.from('analytics-data')
   *
   * // Drop table with purge option (removes all data)
   * const { error: dropError } = await catalog.dropTable(
   *   { namespace: ['default'], name: 'events' },
   *   { purge: true }
   * )
   *
   * if (dropError?.isNotFound()) {
   *   console.log('Table does not exist')
   * }
   *
   * // Drop namespace (must be empty)
   * await catalog.dropNamespace({ namespace: ['default'] })
   * ```
   *
   * @remarks
   * This method provides a bridge between Supabase's bucket management and the standard
   * Apache Iceberg REST Catalog API. The bucket name maps to the Iceberg warehouse parameter.
   * All authentication and configuration is handled automatically using your Supabase credentials.
   *
   * **Error Handling**: Invalid bucket names throw immediately. All catalog
   * operations return `{ data, error }` where errors are `IcebergError` instances from iceberg-js.
   * Use helper methods like `error.isNotFound()` or check `error.status` for specific error handling.
   * Use `.throwOnError()` on the analytics client if you prefer exceptions for catalog operations.
   *
   * **Cleanup Operations**: When using `dropTable`, the `purge: true` option permanently
   * deletes all table data. Without it, the table is marked as deleted but data remains.
   *
   * **Library Dependency**: The returned catalog wraps `IcebergRestCatalog` from iceberg-js.
   * For complete API documentation and advanced usage, refer to the
   * [iceberg-js documentation](https://supabase.github.io/iceberg-js/).
   */
  from(bucketName: string): WrappedIcebergRestCatalog;
}
//#endregion
//#region src/packages/VectorIndexApi.d.ts
/**
 * @alpha
 *
 * Options for creating a vector index
 *
 * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
 */
interface CreateIndexOptions {
  vectorBucketName: string;
  indexName: string;
  dataType: VectorDataType;
  dimension: number;
  distanceMetric: DistanceMetric;
  metadataConfiguration?: MetadataConfiguration;
}
/**
 * @hidden
 * Base implementation for vector index operations.
 * Use {@link VectorBucketScope} via `supabase.storage.vectors.from('bucket')` instead.
 */
declare class VectorIndexApi extends BaseApiClient<StorageError> {
  /** Creates a new VectorIndexApi instance */
  constructor(url: string, headers?: {
    [key: string]: string;
  }, fetch?: Fetch);
  /** Creates a new vector index within a bucket */
  createIndex(options: CreateIndexOptions): Promise<ApiResponse<undefined>>;
  /** Retrieves metadata for a specific vector index */
  getIndex(vectorBucketName: string, indexName: string): Promise<ApiResponse<{
    index: VectorIndex;
  }>>;
  /** Lists vector indexes within a bucket with optional filtering and pagination */
  listIndexes(options: ListIndexesOptions): Promise<ApiResponse<ListIndexesResponse>>;
  /** Deletes a vector index and all its data */
  deleteIndex(vectorBucketName: string, indexName: string): Promise<ApiResponse<undefined>>;
}
//#endregion
//#region src/packages/VectorDataApi.d.ts
/**
 * @hidden
 * Base implementation for vector data operations.
 * Use {@link VectorIndexScope} via `supabase.storage.vectors.from('bucket').index('idx')` instead.
 */
declare class VectorDataApi extends BaseApiClient<StorageError> {
  /** Creates a new VectorDataApi instance */
  constructor(url: string, headers?: {
    [key: string]: string;
  }, fetch?: Fetch);
  /** Inserts or updates vectors in batch (1-500 per request) */
  putVectors(options: PutVectorsOptions): Promise<ApiResponse<undefined>>;
  /** Retrieves vectors by their keys in batch */
  getVectors(options: GetVectorsOptions): Promise<ApiResponse<GetVectorsResponse>>;
  /** Lists vectors in an index with pagination */
  listVectors(options: ListVectorsOptions): Promise<ApiResponse<ListVectorsResponse>>;
  /** Queries for similar vectors using approximate nearest neighbor search */
  queryVectors(options: QueryVectorsOptions): Promise<ApiResponse<QueryVectorsResponse>>;
  /** Deletes vectors by their keys in batch (1-500 per request) */
  deleteVectors(options: DeleteVectorsOptions): Promise<ApiResponse<undefined>>;
}
//#endregion
//#region src/packages/VectorBucketApi.d.ts
/**
 * @hidden
 * Base implementation for vector bucket operations.
 * Use {@link StorageVectorsClient} via `supabase.storage.vectors` instead.
 */
declare class VectorBucketApi extends BaseApiClient<StorageError> {
  /** Creates a new VectorBucketApi instance */
  constructor(url: string, headers?: {
    [key: string]: string;
  }, fetch?: Fetch);
  /** Creates a new vector bucket */
  createBucket(vectorBucketName: string): Promise<ApiResponse<undefined>>;
  /** Retrieves metadata for a specific vector bucket */
  getBucket(vectorBucketName: string): Promise<ApiResponse<{
    vectorBucket: VectorBucket;
  }>>;
  /** Lists vector buckets with optional filtering and pagination */
  listBuckets(options?: ListVectorBucketsOptions): Promise<ApiResponse<ListVectorBucketsResponse>>;
  /** Deletes a vector bucket (must be empty first) */
  deleteBucket(vectorBucketName: string): Promise<ApiResponse<undefined>>;
}
//#endregion
//#region src/packages/StorageVectorsClient.d.ts
/**
 *
 * @alpha
 *
 * Configuration options for the Storage Vectors client
 *
 * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
 */
interface StorageVectorsClientOptions {
  /**
   * Custom headers to include in all requests
   */
  headers?: {
    [key: string]: string;
  };
  /**
   * Custom fetch implementation (optional)
   * Useful for testing or custom request handling
   */
  fetch?: Fetch;
}
/**
 *
 * @alpha
 *
 * Main client for interacting with S3 Vectors API
 * Provides access to bucket, index, and vector data operations
 *
 * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
 *
 * **Usage Patterns:**
 *
 * ```typescript
 * const { data, error } = await supabase
 *  .storage
 *  .vectors
 *  .createBucket('embeddings-prod')
 *
 * // Access index operations via buckets
 * const bucket = supabase.storage.vectors.from('embeddings-prod')
 * await bucket.createIndex({
 *   indexName: 'documents',
 *   dataType: 'float32',
 *   dimension: 1536,
 *   distanceMetric: 'cosine'
 * })
 *
 * // Access vector operations via index
 * const index = bucket.index('documents')
 * await index.putVectors({
 *   vectors: [
 *     { key: 'doc-1', data: { float32: [...] }, metadata: { title: 'Intro' } }
 *   ]
 * })
 *
 * // Query similar vectors
 * const { data } = await index.queryVectors({
 *   queryVector: { float32: [...] },
 *   topK: 5,
 *   returnDistance: true
 * })
 * ```
 */
declare class StorageVectorsClient extends VectorBucketApi {
  /**
   * @alpha
   *
   * Creates a StorageVectorsClient that can manage buckets, indexes, and vectors.
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param url - Base URL of the Storage Vectors REST API.
   * @param options.headers - Optional headers (for example `Authorization`) applied to every request.
   * @param options.fetch - Optional custom `fetch` implementation for non-browser runtimes.
   *
   * @example Using supabase-js (recommended)
   * ```typescript
   * import { createClient } from '@supabase/supabase-js'
   *
   * const supabase = createClient('https://xyzcompany.supabase.co', 'your-publishable-key')
   * const bucket = supabase.storage.vectors.from('embeddings-prod')
   * ```
   *
   * @example Standalone import for bundle-sensitive environments
   * ```typescript
   * import { StorageVectorsClient } from '@supabase/storage-js'
   *
   * const client = new StorageVectorsClient(url, options)
   * ```
   */
  constructor(url: string, options?: StorageVectorsClientOptions);
  /**
   *
   * @alpha
   *
   * Access operations for a specific vector bucket
   * Returns a scoped client for index and vector operations within the bucket
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param vectorBucketName - Name of the vector bucket
   * @returns Bucket-scoped client with index and vector operations
   *
   * @example Accessing a vector bucket
   * ```typescript
   * const bucket = supabase.storage.vectors.from('embeddings-prod')
   * ```
   */
  from(vectorBucketName: string): VectorBucketScope;
  /**
   *
   * @alpha
   *
   * Creates a new vector bucket
   * Vector buckets are containers for vector indexes and their data
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param vectorBucketName - Unique name for the vector bucket
   * @returns Promise with empty response on success or error
   *
   * @example Creating a vector bucket
   * ```typescript
   * const { data, error } = await supabase
   *   .storage
   *   .vectors
   *   .createBucket('embeddings-prod')
   * ```
   */
  createBucket(vectorBucketName: string): Promise<ApiResponse<undefined>>;
  /**
   *
   * @alpha
   *
   * Retrieves metadata for a specific vector bucket
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param vectorBucketName - Name of the vector bucket
   * @returns Promise with bucket metadata or error
   *
   * @example Get bucket metadata
   * ```typescript
   * const { data, error } = await supabase
   *   .storage
   *   .vectors
   *   .getBucket('embeddings-prod')
   *
   * console.log('Bucket created:', data?.vectorBucket.creationTime)
   * ```
   */
  getBucket(vectorBucketName: string): Promise<ApiResponse<{
    vectorBucket: VectorBucket;
  }>>;
  /**
   *
   * @alpha
   *
   * Lists all vector buckets with optional filtering and pagination
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param options - Optional filters (prefix, maxResults, nextToken)
   * @returns Promise with list of buckets or error
   *
   * @example List vector buckets
   * ```typescript
   * const { data, error } = await supabase
   *   .storage
   *   .vectors
   *   .listBuckets({ prefix: 'embeddings-' })
   *
   * data?.vectorBuckets.forEach(bucket => {
   *   console.log(bucket.vectorBucketName)
   * })
   * ```
   */
  listBuckets(options?: ListVectorBucketsOptions): Promise<ApiResponse<ListVectorBucketsResponse>>;
  /**
   *
   * @alpha
   *
   * Deletes a vector bucket (bucket must be empty)
   * All indexes must be deleted before deleting the bucket
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param vectorBucketName - Name of the vector bucket to delete
   * @returns Promise with empty response on success or error
   *
   * @example Delete a vector bucket
   * ```typescript
   * const { data, error } = await supabase
   *   .storage
   *   .vectors
   *   .deleteBucket('embeddings-old')
   * ```
   */
  deleteBucket(vectorBucketName: string): Promise<ApiResponse<undefined>>;
}
/**
 *
 * @alpha
 *
 * Scoped client for operations within a specific vector bucket
 * Provides index management and access to vector operations
 *
 * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
 */
declare class VectorBucketScope extends VectorIndexApi {
  private vectorBucketName;
  /**
   * @alpha
   *
   * Creates a helper that automatically scopes all index operations to the provided bucket.
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @example Creating a vector bucket scope
   * ```typescript
   * const bucket = supabase.storage.vectors.from('embeddings-prod')
   * ```
   */
  constructor(url: string, headers: {
    [key: string]: string;
  }, vectorBucketName: string, fetch?: Fetch);
  /**
   *
   * @alpha
   *
   * Creates a new vector index in this bucket
   * Convenience method that automatically includes the bucket name
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param options - Index configuration (vectorBucketName is automatically set)
   * @returns Promise with empty response on success or error
   *
   * @example Creating a vector index
   * ```typescript
   * const bucket = supabase.storage.vectors.from('embeddings-prod')
   * await bucket.createIndex({
   *   indexName: 'documents-openai',
   *   dataType: 'float32',
   *   dimension: 1536,
   *   distanceMetric: 'cosine',
   *   metadataConfiguration: {
   *     nonFilterableMetadataKeys: ['raw_text']
   *   }
   * })
   * ```
   */
  createIndex(options: Omit<CreateIndexOptions, 'vectorBucketName'>): Promise<ApiResponse<undefined>>;
  /**
   *
   * @alpha
   *
   * Lists indexes in this bucket
   * Convenience method that automatically includes the bucket name
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param options - Listing options (vectorBucketName is automatically set)
   * @returns Promise with response containing indexes array and pagination token or error
   *
   * @example List indexes
   * ```typescript
   * const bucket = supabase.storage.vectors.from('embeddings-prod')
   * const { data } = await bucket.listIndexes({ prefix: 'documents-' })
   * ```
   */
  listIndexes(options?: Omit<ListIndexesOptions, 'vectorBucketName'>): Promise<ApiResponse<ListIndexesResponse>>;
  /**
   *
   * @alpha
   *
   * Retrieves metadata for a specific index in this bucket
   * Convenience method that automatically includes the bucket name
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param indexName - Name of the index to retrieve
   * @returns Promise with index metadata or error
   *
   * @example Get index metadata
   * ```typescript
   * const bucket = supabase.storage.vectors.from('embeddings-prod')
   * const { data } = await bucket.getIndex('documents-openai')
   * console.log('Dimension:', data?.index.dimension)
   * ```
   */
  getIndex(indexName: string): Promise<ApiResponse<{
    index: VectorIndex;
  }>>;
  /**
   *
   * @alpha
   *
   * Deletes an index from this bucket
   * Convenience method that automatically includes the bucket name
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param indexName - Name of the index to delete
   * @returns Promise with empty response on success or error
   *
   * @example Delete an index
   * ```typescript
   * const bucket = supabase.storage.vectors.from('embeddings-prod')
   * await bucket.deleteIndex('old-index')
   * ```
   */
  deleteIndex(indexName: string): Promise<ApiResponse<undefined>>;
  /**
   *
   * @alpha
   *
   * Access operations for a specific index within this bucket
   * Returns a scoped client for vector data operations
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param indexName - Name of the index
   * @returns Index-scoped client with vector data operations
   *
   * @example Accessing an index
   * ```typescript
   * const index = supabase.storage.vectors.from('embeddings-prod').index('documents-openai')
   *
   * // Insert vectors
   * await index.putVectors({
   *   vectors: [
   *     { key: 'doc-1', data: { float32: [...] }, metadata: { title: 'Intro' } }
   *   ]
   * })
   *
   * // Query similar vectors
   * const { data } = await index.queryVectors({
   *   queryVector: { float32: [...] },
   *   topK: 5
   * })
   * ```
   */
  index(indexName: string): VectorIndexScope;
}
/**
 *
 * @alpha
 *
 * Scoped client for operations within a specific vector index
 * Provides vector data operations (put, get, list, query, delete)
 *
 * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
 */
declare class VectorIndexScope extends VectorDataApi {
  private vectorBucketName;
  private indexName;
  /**
   *
   * @alpha
   *
   * Creates a helper that automatically scopes all vector operations to the provided bucket/index names.
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @example Creating a vector index scope
   * ```typescript
   * const index = supabase.storage.vectors.from('embeddings-prod').index('documents-openai')
   * ```
   */
  constructor(url: string, headers: {
    [key: string]: string;
  }, vectorBucketName: string, indexName: string, fetch?: Fetch);
  /**
   *
   * @alpha
   *
   * Inserts or updates vectors in this index
   * Convenience method that automatically includes bucket and index names
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param options - Vector insertion options (bucket and index names automatically set)
   * @returns Promise with empty response on success or error
   *
   * @example Insert vectors into an index
   * ```typescript
   * const index = supabase.storage.vectors.from('embeddings-prod').index('documents-openai')
   * await index.putVectors({
   *   vectors: [
   *     {
   *       key: 'doc-1',
   *       data: { float32: [0.1, 0.2, ...] },
   *       metadata: { title: 'Introduction', page: 1 }
   *     }
   *   ]
   * })
   * ```
   */
  putVectors(options: Omit<PutVectorsOptions, 'vectorBucketName' | 'indexName'>): Promise<ApiResponse<undefined>>;
  /**
   *
   * @alpha
   *
   * Retrieves vectors by keys from this index
   * Convenience method that automatically includes bucket and index names
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param options - Vector retrieval options (bucket and index names automatically set)
   * @returns Promise with response containing vectors array or error
   *
   * @example Get vectors by keys
   * ```typescript
   * const index = supabase.storage.vectors.from('embeddings-prod').index('documents-openai')
   * const { data } = await index.getVectors({
   *   keys: ['doc-1', 'doc-2'],
   *   returnMetadata: true
   * })
   * ```
   */
  getVectors(options: Omit<GetVectorsOptions, 'vectorBucketName' | 'indexName'>): Promise<ApiResponse<GetVectorsResponse>>;
  /**
   *
   * @alpha
   *
   * Lists vectors in this index with pagination
   * Convenience method that automatically includes bucket and index names
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param options - Listing options (bucket and index names automatically set)
   * @returns Promise with response containing vectors array and pagination token or error
   *
   * @example List vectors with pagination
   * ```typescript
   * const index = supabase.storage.vectors.from('embeddings-prod').index('documents-openai')
   * const { data } = await index.listVectors({
   *   maxResults: 500,
   *   returnMetadata: true
   * })
   * ```
   */
  listVectors(options?: Omit<ListVectorsOptions, 'vectorBucketName' | 'indexName'>): Promise<ApiResponse<ListVectorsResponse>>;
  /**
   *
   * @alpha
   *
   * Queries for similar vectors in this index
   * Convenience method that automatically includes bucket and index names
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param options - Query options (bucket and index names automatically set)
   * @returns Promise with response containing vectors ordered by distance, an optional pagination token, or an error
   *
   * @example Query similar vectors
   * ```typescript
   * const index = supabase.storage.vectors.from('embeddings-prod').index('documents-openai')
   * const { data } = await index.queryVectors({
   *   queryVector: { float32: [0.1, 0.2, ...] },
   *   topK: 5,
   *   filter: { category: 'technical' },
   *   returnDistance: true,
   *   returnMetadata: true
   * })
   * ```
   */
  queryVectors(options: Omit<QueryVectorsOptions, 'vectorBucketName' | 'indexName'>): Promise<ApiResponse<QueryVectorsResponse>>;
  /**
   *
   * @alpha
   *
   * Deletes vectors by keys from this index
   * Convenience method that automatically includes bucket and index names
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   * @param options - Deletion options (bucket and index names automatically set)
   * @returns Promise with empty response on success or error
   *
   * @example Delete vectors by keys
   * ```typescript
   * const index = supabase.storage.vectors.from('embeddings-prod').index('documents-openai')
   * await index.deleteVectors({
   *   keys: ['doc-1', 'doc-2', 'doc-3']
   * })
   * ```
   */
  deleteVectors(options: Omit<DeleteVectorsOptions, 'vectorBucketName' | 'indexName'>): Promise<ApiResponse<undefined>>;
}
//#endregion
//#region src/StorageClient.d.ts
interface StorageClientOptions {
  useNewHostname?: boolean;
}
declare class StorageClient extends StorageBucketApi {
  /**
   * Creates a client for Storage buckets, files, analytics, and vectors.
   *
   * @category Storage
   * @subcategory File Buckets
   *
   * @example Using supabase-js (recommended)
   * ```ts
   * import { createClient } from '@supabase/supabase-js'
   *
   * const supabase = createClient('https://xyzcompany.supabase.co', 'your-publishable-key')
   * const avatars = supabase.storage.from('avatars')
   * ```
   *
   * @example Standalone import for bundle-sensitive environments
   * ```ts
   * import { StorageClient } from '@supabase/storage-js'
   *
   * const storage = new StorageClient('https://xyzcompany.supabase.co/storage/v1', {
   *   apikey: 'your-publishable-key',
   * })
   * const avatars = storage.from('avatars')
   * ```
   */
  constructor(url: string, headers?: {
    [key: string]: string;
  }, fetch?: Fetch, opts?: StorageClientOptions);
  /**
   * Perform file operation in a bucket.
   *
   * @category Storage
   * @subcategory File Buckets
   *
   * @param id The bucket id to operate on.
   *
   * @example Accessing a bucket
   * ```typescript
   * const avatars = supabase.storage.from('avatars')
   * ```
   */
  from(id: string): StorageFileApi;
  /**
   *
   * @alpha
   *
   * Access vector storage operations.
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Vector Buckets
   *
   * @returns A StorageVectorsClient instance configured with the current storage settings.
   */
  get vectors(): StorageVectorsClient;
  /**
   *
   * @alpha
   *
   * Access analytics storage operations using Iceberg tables.
   *
   * **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
   *
   * @category Storage
   * @subcategory Analytics Buckets
   *
   * @returns A StorageAnalyticsClient instance configured with the current storage settings.
   */
  get analytics(): StorageAnalyticsClient;
}
//#endregion
export { AnalyticBucket, ApiResponse, Bucket, BucketLifecycleConfiguration, BucketType, Camelize, type CreateIndexOptions, CreateSettableVersioningStatus, DeleteObjectEntry, DeleteVectorsOptions, DestinationOptions, DistanceMetric, DownloadResult, EncryptionConfiguration, ErrorNamespace, ErrorResponse, FetchParameters, FileMetadata, FileObject, FileObjectV2, FileOptions, GetVectorsOptions, GetVectorsResponse, LifecycleRule, LifecycleRuleFilter, LifecycleRuleStatus, ListBucketOptions, ListIndexesOptions, ListIndexesResponse, ListVectorBucketsOptions, ListVectorBucketsResponse, ListVectorsOptions, ListVectorsResponse, Metadata, MetadataConfiguration, NoncurrentVersionExpiration, PurgeCacheOptions, PutVectorsOptions, QueryVectorsOptions, QueryVectorsResponse, SearchOptions, SearchV2Folder, SearchV2Object, SearchV2Options, SearchV2Result, SortBy, SortByV2, StorageAnalyticsClient, StorageApiError, StorageClient, type StorageClientOptions, StorageError, StorageUnknownError, StorageVectorsApiError, StorageVectorsClient, type StorageVectorsClientOptions, StorageVectorsError, StorageVectorsErrorCode, StorageVectorsUnknownError, SuccessResponse, TransformOptions, UpdateSettableVersioningStatus, VectorBucket, VectorBucketApi, VectorBucketScope, VectorData, VectorDataApi, VectorDataType, VectorFetchParameters, VectorFilter, VectorIndex, VectorIndexApi, VectorIndexScope, VectorMatch, VectorMetadata, VectorObject, VersioningStatus, isStorageError, isStorageVectorsError };
//# sourceMappingURL=index.d.cts.map