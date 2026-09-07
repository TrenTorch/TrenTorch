import { IcebergRestCatalog } from "iceberg-js";

//#region \0@oxc-project+runtime@0.103.0/helpers/typeof.js
function _typeof(o) {
	"@babel/helpers - typeof";
	return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(o$1) {
		return typeof o$1;
	} : function(o$1) {
		return o$1 && "function" == typeof Symbol && o$1.constructor === Symbol && o$1 !== Symbol.prototype ? "symbol" : typeof o$1;
	}, _typeof(o);
}

//#endregion
//#region \0@oxc-project+runtime@0.103.0/helpers/toPrimitive.js
function toPrimitive(t, r) {
	if ("object" != _typeof(t) || !t) return t;
	var e = t[Symbol.toPrimitive];
	if (void 0 !== e) {
		var i = e.call(t, r || "default");
		if ("object" != _typeof(i)) return i;
		throw new TypeError("@@toPrimitive must return a primitive value.");
	}
	return ("string" === r ? String : Number)(t);
}

//#endregion
//#region \0@oxc-project+runtime@0.103.0/helpers/toPropertyKey.js
function toPropertyKey(t) {
	var i = toPrimitive(t, "string");
	return "symbol" == _typeof(i) ? i : i + "";
}

//#endregion
//#region \0@oxc-project+runtime@0.103.0/helpers/defineProperty.js
function _defineProperty(e, r, t) {
	return (r = toPropertyKey(r)) in e ? Object.defineProperty(e, r, {
		value: t,
		enumerable: !0,
		configurable: !0,
		writable: !0
	}) : e[r] = t, e;
}

//#endregion
//#region \0@oxc-project+runtime@0.103.0/helpers/objectSpread2.js
function ownKeys(e, r) {
	var t = Object.keys(e);
	if (Object.getOwnPropertySymbols) {
		var o = Object.getOwnPropertySymbols(e);
		r && (o = o.filter(function(r$1) {
			return Object.getOwnPropertyDescriptor(e, r$1).enumerable;
		})), t.push.apply(t, o);
	}
	return t;
}
function _objectSpread2(e) {
	for (var r = 1; r < arguments.length; r++) {
		var t = null != arguments[r] ? arguments[r] : {};
		r % 2 ? ownKeys(Object(t), !0).forEach(function(r$1) {
			_defineProperty(e, r$1, t[r$1]);
		}) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(t)) : ownKeys(Object(t)).forEach(function(r$1) {
			Object.defineProperty(e, r$1, Object.getOwnPropertyDescriptor(t, r$1));
		});
	}
	return e;
}

//#endregion
//#region src/lib/common/errors.ts
/**
* Base error class for all Storage errors
* Supports both 'storage' and 'vectors' namespaces
*/
var StorageError = class extends Error {
	constructor(message, namespace = "storage", status, statusCode) {
		super(message);
		this.__isStorageError = true;
		this.namespace = namespace;
		this.name = namespace === "vectors" ? "StorageVectorsError" : "StorageError";
		this.status = status;
		this.statusCode = statusCode;
	}
	toJSON() {
		return {
			name: this.name,
			message: this.message,
			status: this.status,
			statusCode: this.statusCode
		};
	}
};
/**
* Type guard to check if an error is a StorageError
* @param error - The error to check
* @returns True if the error is a StorageError
*/
function isStorageError(error) {
	return typeof error === "object" && error !== null && "__isStorageError" in error;
}
/**
* API error returned from Storage service
* Includes HTTP status code and service-specific error code
*/
var StorageApiError = class extends StorageError {
	constructor(message, status, statusCode, namespace = "storage", code) {
		super(message, namespace, status, statusCode);
		this.name = namespace === "vectors" ? "StorageVectorsApiError" : "StorageApiError";
		this.status = status;
		this.statusCode = statusCode;
		this.code = code;
	}
	toJSON() {
		return _objectSpread2(_objectSpread2({}, super.toJSON()), {}, { code: this.code });
	}
};
/**
* Unknown error that doesn't match expected error patterns
* Wraps the original error for debugging
*/
var StorageUnknownError = class extends StorageError {
	constructor(message, originalError, namespace = "storage") {
		super(message, namespace);
		this.name = namespace === "vectors" ? "StorageVectorsUnknownError" : "StorageUnknownError";
		this.originalError = originalError;
	}
};
/**
* @deprecated Use StorageError with namespace='vectors' instead
* Alias for backward compatibility with existing vector storage code
*/
var StorageVectorsError = class extends StorageError {
	constructor(message) {
		super(message, "vectors");
	}
};
/**
* Type guard to check if an error is a StorageVectorsError
* @param error - The error to check
* @returns True if the error is a StorageVectorsError
*/
function isStorageVectorsError(error) {
	return isStorageError(error) && error["namespace"] === "vectors";
}
/**
* @deprecated Use StorageApiError with namespace='vectors' instead
* Alias for backward compatibility with existing vector storage code
*/
var StorageVectorsApiError = class extends StorageApiError {
	constructor(message, status, statusCode) {
		super(message, status, statusCode, "vectors");
	}
};
/**
* @deprecated Use StorageUnknownError with namespace='vectors' instead
* Alias for backward compatibility with existing vector storage code
*/
var StorageVectorsUnknownError = class extends StorageUnknownError {
	constructor(message, originalError) {
		super(message, originalError, "vectors");
	}
};
/**
* Error codes specific to S3 Vectors API
* Maps AWS service errors to application-friendly error codes
*/
let StorageVectorsErrorCode = /* @__PURE__ */ function(StorageVectorsErrorCode$1) {
	/** Internal server fault (HTTP 500) */
	StorageVectorsErrorCode$1["InternalError"] = "InternalError";
	/** Resource already exists / conflict (HTTP 409) */
	StorageVectorsErrorCode$1["S3VectorConflictException"] = "S3VectorConflictException";
	/** Resource not found (HTTP 404) */
	StorageVectorsErrorCode$1["S3VectorNotFoundException"] = "S3VectorNotFoundException";
	/** Delete bucket while not empty (HTTP 400) */
	StorageVectorsErrorCode$1["S3VectorBucketNotEmpty"] = "S3VectorBucketNotEmpty";
	/** Exceeds bucket quota/limit (HTTP 400) */
	StorageVectorsErrorCode$1["S3VectorMaxBucketsExceeded"] = "S3VectorMaxBucketsExceeded";
	/** Exceeds index quota/limit (HTTP 400) */
	StorageVectorsErrorCode$1["S3VectorMaxIndexesExceeded"] = "S3VectorMaxIndexesExceeded";
	return StorageVectorsErrorCode$1;
}({});

//#endregion
//#region src/lib/common/headers.ts
/**
* Sets a header with case-insensitive deduplication.
* Removes any existing headers whose name matches (case-insensitive),
* then sets the value under the lowercase key. Does not mutate the input object.
*
* @param headers - Existing headers object
* @param name - Header name to set (stored as lowercase)
* @param value - Header value
* @returns New headers object with the header set
*/
function setHeader(headers, name, value) {
	const result = _objectSpread2({}, headers);
	const nameLower = name.toLowerCase();
	for (const key of Object.keys(result)) if (key.toLowerCase() === nameLower) delete result[key];
	result[nameLower] = value;
	return result;
}
/**
* Normalizes all header keys to lowercase with case-insensitive deduplication.
* When duplicate keys exist (differing only in case), the last value wins.
* Does not mutate the input object.
*
* @param headers - Headers object to normalize
* @returns New headers object with all keys lowercased
*/
function normalizeHeaders(headers) {
	const result = {};
	for (const [key, value] of Object.entries(headers)) result[key.toLowerCase()] = value;
	return result;
}

//#endregion
//#region src/lib/common/helpers.ts
/**
* Resolves the fetch implementation to use
* Uses custom fetch if provided, otherwise uses native fetch
*
* @param customFetch - Optional custom fetch implementation
* @returns Resolved fetch function
*/
const resolveFetch = (customFetch) => {
	if (customFetch) return (...args) => customFetch(...args);
	return (...args) => fetch(...args);
};
/**
* Determine if input is a plain object
* An object is plain if it's created by either {}, new Object(), or Object.create(null)
*
* @param value - Value to check
* @returns True if value is a plain object
* @source https://github.com/sindresorhus/is-plain-obj
*/
const isPlainObject = (value) => {
	if (typeof value !== "object" || value === null) return false;
	const prototype = Object.getPrototypeOf(value);
	return (prototype === null || prototype === Object.prototype || Object.getPrototypeOf(prototype) === null) && !(Symbol.toStringTag in value) && !(Symbol.iterator in value);
};
/**
* Recursively converts object keys from snake_case to camelCase
* Used for normalizing API responses
*
* @param item - Object to convert
* @returns Converted object with camelCase keys
*/
const recursiveToCamel = (item) => {
	if (Array.isArray(item)) return item.map((el) => recursiveToCamel(el));
	else if (typeof item === "function" || item !== Object(item)) return item;
	const result = {};
	Object.entries(item).forEach(([key, value]) => {
		const newKey = key.replace(/([-_][a-z])/gi, (c) => c.toUpperCase().replace(/[-_]/g, ""));
		result[newKey] = recursiveToCamel(value);
	});
	return result;
};
/**
* Validates if a given bucket name is valid according to Supabase Storage API rules
* Mirrors backend validation from: storage/src/storage/limits.ts:isValidBucketName()
*
* Rules:
* - Length: 1-100 characters
* - Allowed characters: alphanumeric (a-z, A-Z, 0-9), underscore (_), and safe special characters
* - Safe special characters: ! - . * ' ( ) space & $ @ = ; : + , ?
* - Forbidden: path separators (/, \), path traversal (..), leading/trailing whitespace
*
* AWS S3 Reference: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html
*
* @param bucketName - The bucket name to validate
* @returns true if valid, false otherwise
*/
const isValidBucketName = (bucketName) => {
	if (!bucketName || typeof bucketName !== "string") return false;
	if (bucketName.length === 0 || bucketName.length > 100) return false;
	if (bucketName.trim() !== bucketName) return false;
	if (bucketName.includes("/") || bucketName.includes("\\")) return false;
	return /^[\w!.\*'() &$@=;:+,?-]+$/.test(bucketName);
};
/**
* Percent-encodes each segment of a storage path so URL delimiters within a
* key (e.g. `?`, `#`) can't be interpreted as a querystring/fragment start.
*
* Splits on `/` so real path separators stay literal — the storage server
* routes on them and decodes each segment back to the original key.
*
* @param path - A bucket id or `bucketId/objectKey` path
* @returns The path with each `/`-delimited segment percent-encoded
*/
const encodeStoragePath = (path) => path.split("/").map(encodeURIComponent).join("/");

//#endregion
//#region src/lib/common/fetch.ts
/**
* Extracts error message from various error response formats
* @param err - Error object from API
* @returns Human-readable error message
*/
const _getErrorMessage = (err) => {
	if (typeof err === "object" && err !== null) {
		const e = err;
		if (typeof e.msg === "string") return e.msg;
		if (typeof e.message === "string") return e.message;
		if (typeof e.error_description === "string") return e.error_description;
		if (typeof e.error === "string") return e.error;
		if (typeof e.error === "object" && e.error !== null) {
			const nested = e.error;
			if (typeof nested.message === "string") return nested.message;
		}
	}
	return JSON.stringify(err);
};
/**
* Handles fetch errors and converts them to Storage error types
* @param error - The error caught from fetch
* @param reject - Promise rejection function
* @param options - Fetch options that may affect error handling
* @param namespace - Error namespace ('storage' or 'vectors')
*/
const handleError = async (error, reject, options, namespace) => {
	if (error !== null && typeof error === "object" && "json" in error && typeof error.json === "function") {
		const responseError = error;
		let status = parseInt(String(responseError.status), 10);
		if (!Number.isFinite(status)) status = 500;
		responseError.json().then((err) => {
			const statusCode = (err === null || err === void 0 ? void 0 : err.statusCode) || (err === null || err === void 0 ? void 0 : err.code) || status + "";
			reject(new StorageApiError(_getErrorMessage(err), status, statusCode, namespace, err === null || err === void 0 ? void 0 : err.code));
		}).catch(() => {
			const statusCode = status + "";
			reject(new StorageApiError(responseError.statusText || `HTTP ${status} error`, status, statusCode, namespace));
		});
	} else reject(new StorageUnknownError(_getErrorMessage(error), error, namespace));
};
/**
* Builds request parameters for fetch calls
* @param method - HTTP method
* @param options - Custom fetch options
* @param parameters - Additional fetch parameters like AbortSignal
* @param body - Request body (will be JSON stringified if plain object)
* @returns Complete fetch request parameters
*/
const _getRequestParams = (method, options, parameters, body) => {
	const params = {
		method,
		headers: (options === null || options === void 0 ? void 0 : options.headers) || {}
	};
	if (method === "GET" || method === "HEAD" || !body) return _objectSpread2(_objectSpread2({}, params), parameters);
	if (isPlainObject(body)) {
		var _contentType;
		const headers = (options === null || options === void 0 ? void 0 : options.headers) || {};
		let contentType;
		for (const [key, value] of Object.entries(headers)) if (key.toLowerCase() === "content-type") contentType = value;
		params.headers = setHeader(headers, "Content-Type", (_contentType = contentType) !== null && _contentType !== void 0 ? _contentType : "application/json");
		params.body = JSON.stringify(body);
	} else params.body = body;
	if (options === null || options === void 0 ? void 0 : options.duplex) params.duplex = options.duplex;
	return _objectSpread2(_objectSpread2({}, params), parameters);
};
/**
* Internal request handler that wraps fetch with error handling
* @param fetcher - Fetch function to use
* @param method - HTTP method
* @param url - Request URL
* @param options - Custom fetch options
* @param parameters - Additional fetch parameters
* @param body - Request body
* @param namespace - Error namespace ('storage' or 'vectors')
* @returns Promise with parsed response or error
*/
async function _handleRequest(fetcher, method, url, options, parameters, body, namespace) {
	return new Promise((resolve, reject) => {
		fetcher(url, _getRequestParams(method, options, parameters, body)).then((result) => {
			if (!result.ok) throw result;
			if (options === null || options === void 0 ? void 0 : options.noResolveJson) return result;
			if (namespace === "vectors") {
				const contentType = result.headers.get("content-type");
				if (result.headers.get("content-length") === "0" || result.status === 204) return {};
				if (!contentType || !contentType.includes("application/json")) return {};
			}
			return result.json();
		}).then((data) => resolve(data)).catch((error) => handleError(error, reject, options, namespace));
	});
}
/**
* Creates a fetch API with the specified namespace
* @param namespace - Error namespace ('storage' or 'vectors')
* @returns Object with HTTP method functions
*/
function createFetchApi(namespace = "storage") {
	return {
		get: async (fetcher, url, options, parameters) => {
			return _handleRequest(fetcher, "GET", url, options, parameters, void 0, namespace);
		},
		post: async (fetcher, url, body, options, parameters) => {
			return _handleRequest(fetcher, "POST", url, options, parameters, body, namespace);
		},
		put: async (fetcher, url, body, options, parameters) => {
			return _handleRequest(fetcher, "PUT", url, options, parameters, body, namespace);
		},
		head: async (fetcher, url, options, parameters) => {
			return _handleRequest(fetcher, "HEAD", url, _objectSpread2(_objectSpread2({}, options), {}, { noResolveJson: true }), parameters, void 0, namespace);
		},
		remove: async (fetcher, url, body, options, parameters) => {
			return _handleRequest(fetcher, "DELETE", url, options, parameters, body, namespace);
		}
	};
}
const defaultApi = createFetchApi("storage");
const { get, post, put, head, remove } = defaultApi;
const vectorsApi = createFetchApi("vectors");

//#endregion
//#region src/lib/common/BaseApiClient.ts
/**
* @ignore
* Base API client class for all Storage API classes
* Provides common infrastructure for error handling and configuration
*
* @typeParam TError - The error type (StorageError or subclass)
*/
var BaseApiClient = class {
	/**
	* Creates a new BaseApiClient instance
	* @param url - Base URL for API requests
	* @param headers - Default headers for API requests
	* @param fetch - Optional custom fetch implementation
	* @param namespace - Error namespace ('storage' or 'vectors')
	*/
	constructor(url, headers = {}, fetch$1, namespace = "storage") {
		this.shouldThrowOnError = false;
		this.url = url;
		this.headers = normalizeHeaders(headers);
		this.fetch = resolveFetch(fetch$1);
		this.namespace = namespace;
	}
	/**
	* Enable throwing errors instead of returning them.
	* When enabled, errors are thrown instead of returned in { data, error } format.
	*
	* @returns this - For method chaining
	*/
	throwOnError() {
		this.shouldThrowOnError = true;
		return this;
	}
	/**
	* Set an HTTP header for the request.
	* Creates a shallow copy of headers to avoid mutating shared state.
	*
	* @param name - Header name
	* @param value - Header value
	* @returns this - For method chaining
	*/
	setHeader(name, value) {
		this.headers = setHeader(this.headers, name, value);
		return this;
	}
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
	async handleOperation(operation) {
		var _this = this;
		try {
			return {
				data: await operation(),
				error: null
			};
		} catch (error) {
			if (_this.shouldThrowOnError) throw error;
			if (isStorageError(error)) return {
				data: null,
				error
			};
			throw error;
		}
	}
};

//#endregion
//#region src/packages/StreamDownloadBuilder.ts
let _Symbol$toStringTag$1;
_Symbol$toStringTag$1 = Symbol.toStringTag;
var StreamDownloadBuilder = class {
	constructor(downloadFn, shouldThrowOnError) {
		this.downloadFn = downloadFn;
		this.shouldThrowOnError = shouldThrowOnError;
		this[_Symbol$toStringTag$1] = "StreamDownloadBuilder";
		this.promise = null;
	}
	then(onfulfilled, onrejected) {
		return this.getPromise().then(onfulfilled, onrejected);
	}
	catch(onrejected) {
		return this.getPromise().catch(onrejected);
	}
	finally(onfinally) {
		return this.getPromise().finally(onfinally);
	}
	getPromise() {
		if (!this.promise) this.promise = this.execute();
		return this.promise;
	}
	async execute() {
		var _this = this;
		try {
			return {
				data: (await _this.downloadFn()).body,
				error: null
			};
		} catch (error) {
			if (_this.shouldThrowOnError) throw error;
			if (isStorageError(error)) return {
				data: null,
				error
			};
			throw error;
		}
	}
};

//#endregion
//#region src/packages/BlobDownloadBuilder.ts
let _Symbol$toStringTag;
_Symbol$toStringTag = Symbol.toStringTag;
var BlobDownloadBuilder = class {
	constructor(downloadFn, shouldThrowOnError) {
		this.downloadFn = downloadFn;
		this.shouldThrowOnError = shouldThrowOnError;
		this[_Symbol$toStringTag] = "BlobDownloadBuilder";
		this.promise = null;
	}
	asStream() {
		return new StreamDownloadBuilder(this.downloadFn, this.shouldThrowOnError);
	}
	then(onfulfilled, onrejected) {
		return this.getPromise().then(onfulfilled, onrejected);
	}
	catch(onrejected) {
		return this.getPromise().catch(onrejected);
	}
	finally(onfinally) {
		return this.getPromise().finally(onfinally);
	}
	getPromise() {
		if (!this.promise) this.promise = this.execute();
		return this.promise;
	}
	async execute() {
		var _this = this;
		try {
			return {
				data: await (await _this.downloadFn()).blob(),
				error: null
			};
		} catch (error) {
			if (_this.shouldThrowOnError) throw error;
			if (isStorageError(error)) return {
				data: null,
				error
			};
			throw error;
		}
	}
};

//#endregion
//#region src/packages/StorageFileApi.ts
const DEFAULT_SEARCH_OPTIONS = {
	limit: 100,
	offset: 0,
	sortBy: {
		column: "name",
		order: "asc"
	}
};
const DEFAULT_FILE_OPTIONS = {
	cacheControl: "3600",
	contentType: "text/plain;charset=UTF-8",
	upsert: false
};
var StorageFileApi = class extends BaseApiClient {
	constructor(url, headers = {}, bucketId, fetch$1) {
		super(url, headers, fetch$1, "storage");
		this.bucketId = bucketId;
	}
	/**
	* Uploads a file to an existing bucket or replaces an existing file at the specified path with a new one.
	*
	* @param method HTTP method.
	* @param path The relative file path. Should be of the format `folder/subfolder/filename.png`. The bucket must already exist before attempting to upload.
	* @param fileBody The body of the file to be stored in the bucket.
	*/
	async uploadOrUpdate(method, path, fileBody, fileOptions) {
		var _this = this;
		return _this.handleOperation(async () => {
			let body;
			const options = _objectSpread2(_objectSpread2({}, DEFAULT_FILE_OPTIONS), fileOptions);
			let headers = _objectSpread2(_objectSpread2({}, _this.headers), method === "POST" && { "x-upsert": String(options.upsert) });
			const metadata = options.metadata;
			if (typeof Blob !== "undefined" && fileBody instanceof Blob) {
				body = new FormData();
				body.append("cacheControl", options.cacheControl);
				if (metadata) body.append("metadata", _this.encodeMetadata(metadata));
				body.append("", fileBody);
			} else if (typeof FormData !== "undefined" && fileBody instanceof FormData) {
				body = fileBody;
				if (!body.has("cacheControl")) body.append("cacheControl", options.cacheControl);
				if (metadata && !body.has("metadata")) body.append("metadata", _this.encodeMetadata(metadata));
			} else {
				body = fileBody;
				headers["cache-control"] = `max-age=${options.cacheControl}`;
				headers["content-type"] = options.contentType;
				if (metadata) headers["x-metadata"] = _this.toBase64(_this.encodeMetadata(metadata));
				if ((typeof ReadableStream !== "undefined" && body instanceof ReadableStream || body && typeof body === "object" && "pipe" in body && typeof body.pipe === "function") && !options.duplex) options.duplex = "half";
			}
			if (fileOptions === null || fileOptions === void 0 ? void 0 : fileOptions.headers) for (const [key, value] of Object.entries(fileOptions.headers)) headers = setHeader(headers, key, value);
			const cleanPath = _this._removeEmptyFolders(path);
			const _path = _this._getFinalPath(cleanPath);
			const data = await (method == "PUT" ? put : post)(_this.fetch, `${_this.url}/object/${_path}`, body, _objectSpread2({ headers }, (options === null || options === void 0 ? void 0 : options.duplex) ? { duplex: options.duplex } : {}));
			return {
				path: cleanPath,
				id: data.Id,
				fullPath: data.Key
			};
		});
	}
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
	async upload(path, fileBody, fileOptions) {
		return this.uploadOrUpdate("POST", path, fileBody, fileOptions);
	}
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
	async uploadToSignedUrl(path, token, fileBody, fileOptions) {
		var _this3 = this;
		const cleanPath = _this3._removeEmptyFolders(path);
		const _path = _this3._getFinalPath(cleanPath);
		const url = new URL(_this3.url + `/object/upload/sign/${_path}`);
		url.searchParams.set("token", token);
		return _this3.handleOperation(async () => {
			let body;
			const options = _objectSpread2(_objectSpread2({}, DEFAULT_FILE_OPTIONS), fileOptions);
			let headers = _objectSpread2(_objectSpread2({}, _this3.headers), { "x-upsert": String(options.upsert) });
			const metadata = options.metadata;
			if (typeof Blob !== "undefined" && fileBody instanceof Blob) {
				body = new FormData();
				body.append("cacheControl", options.cacheControl);
				if (metadata) body.append("metadata", _this3.encodeMetadata(metadata));
				body.append("", fileBody);
			} else if (typeof FormData !== "undefined" && fileBody instanceof FormData) {
				body = fileBody;
				if (!body.has("cacheControl")) body.append("cacheControl", options.cacheControl);
				if (metadata && !body.has("metadata")) body.append("metadata", _this3.encodeMetadata(metadata));
			} else {
				body = fileBody;
				headers["cache-control"] = `max-age=${options.cacheControl}`;
				headers["content-type"] = options.contentType;
				if (metadata) headers["x-metadata"] = _this3.toBase64(_this3.encodeMetadata(metadata));
				if ((typeof ReadableStream !== "undefined" && body instanceof ReadableStream || body && typeof body === "object" && "pipe" in body && typeof body.pipe === "function") && !options.duplex) options.duplex = "half";
			}
			if (fileOptions === null || fileOptions === void 0 ? void 0 : fileOptions.headers) for (const [key, value] of Object.entries(fileOptions.headers)) headers = setHeader(headers, key, value);
			return {
				path: cleanPath,
				fullPath: (await put(_this3.fetch, url.toString(), body, _objectSpread2({ headers }, (options === null || options === void 0 ? void 0 : options.duplex) ? { duplex: options.duplex } : {}))).Key
			};
		});
	}
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
	async createSignedUploadUrl(path, options) {
		var _this4 = this;
		return _this4.handleOperation(async () => {
			let _path = _this4._getFinalPath(path);
			const headers = _objectSpread2({}, _this4.headers);
			if (options === null || options === void 0 ? void 0 : options.upsert) headers["x-upsert"] = "true";
			const data = await post(_this4.fetch, `${_this4.url}/object/upload/sign/${_path}`, {}, { headers });
			const url = new URL(_this4.url + data.url);
			const token = url.searchParams.get("token");
			if (!token) throw new StorageError("No token returned by API");
			return {
				signedUrl: url.toString(),
				path,
				token
			};
		});
	}
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
	async update(path, fileBody, fileOptions) {
		return this.uploadOrUpdate("PUT", path, fileBody, fileOptions);
	}
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
	async move(fromPath, toPath, options) {
		var _this6 = this;
		return _this6.handleOperation(async () => {
			return await post(_this6.fetch, `${_this6.url}/object/move`, {
				bucketId: _this6.bucketId,
				sourceKey: fromPath,
				destinationKey: toPath,
				destinationBucket: options === null || options === void 0 ? void 0 : options.destinationBucket,
				sourceVersionId: options === null || options === void 0 ? void 0 : options.sourceVersionId
			}, { headers: _this6.headers });
		});
	}
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
	async copy(fromPath, toPath, options) {
		var _this7 = this;
		return _this7.handleOperation(async () => {
			return { path: (await post(_this7.fetch, `${_this7.url}/object/copy`, {
				bucketId: _this7.bucketId,
				sourceKey: fromPath,
				destinationKey: toPath,
				destinationBucket: options === null || options === void 0 ? void 0 : options.destinationBucket,
				sourceVersionId: options === null || options === void 0 ? void 0 : options.sourceVersionId
			}, { headers: _this7.headers })).Key };
		});
	}
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
	async createSignedUrl(path, expiresIn, options) {
		var _this8 = this;
		return _this8.handleOperation(async () => {
			let _path = _this8._getFinalPath(path);
			const hasTransform = typeof (options === null || options === void 0 ? void 0 : options.transform) === "object" && options.transform !== null && Object.keys(options.transform).length > 0;
			let data = await post(_this8.fetch, `${_this8.url}/object/sign/${_path}`, _objectSpread2(_objectSpread2({ expiresIn }, hasTransform ? { transform: options.transform } : {}), (options === null || options === void 0 ? void 0 : options.versionId) != null ? { versionId: options.versionId } : {}), { headers: _this8.headers });
			const query = new URLSearchParams();
			if (options === null || options === void 0 ? void 0 : options.download) query.set("download", options.download === true ? "" : options.download);
			if ((options === null || options === void 0 ? void 0 : options.cacheNonce) != null) query.set("cacheNonce", String(options.cacheNonce));
			const queryString = query.toString();
			return { signedUrl: encodeURI(`${_this8.url}${data.signedURL}${queryString ? `&${queryString}` : ""}`) };
		});
	}
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
	async createSignedUrls(paths, expiresIn, options) {
		var _this9 = this;
		return _this9.handleOperation(async () => {
			const data = await post(_this9.fetch, `${_this9.url}/object/sign/${_this9.bucketId}`, {
				expiresIn,
				paths
			}, { headers: _this9.headers });
			const query = new URLSearchParams();
			if (options === null || options === void 0 ? void 0 : options.download) query.set("download", options.download === true ? "" : options.download);
			if ((options === null || options === void 0 ? void 0 : options.cacheNonce) != null) query.set("cacheNonce", String(options.cacheNonce));
			const queryString = query.toString();
			return data.map((datum) => _objectSpread2(_objectSpread2({}, datum), {}, { signedUrl: datum.signedURL ? encodeURI(`${_this9.url}${datum.signedURL}${queryString ? `&${queryString}` : ""}`) : null }));
		});
	}
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
	download(path, options, parameters) {
		const renderPath = typeof (options === null || options === void 0 ? void 0 : options.transform) === "object" && options.transform !== null && Object.keys(options.transform).length > 0 ? "render/image/authenticated" : "object";
		const query = new URLSearchParams();
		if (options === null || options === void 0 ? void 0 : options.transform) this.applyTransformOptsToQuery(query, options.transform);
		if ((options === null || options === void 0 ? void 0 : options.cacheNonce) != null) query.set("cacheNonce", String(options.cacheNonce));
		if ((options === null || options === void 0 ? void 0 : options.versionId) != null) query.set("versionId", String(options.versionId));
		const queryString = query.toString();
		const _path = this._getFinalPath(path);
		const downloadFn = () => get(this.fetch, `${this.url}/${renderPath}/${_path}${queryString ? `?${queryString}` : ""}`, {
			headers: this.headers,
			noResolveJson: true
		}, parameters);
		return new BlobDownloadBuilder(downloadFn, this.shouldThrowOnError);
	}
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
	async info(path, options) {
		var _this10 = this;
		const _path = _this10._getFinalPath(path);
		const query = new URLSearchParams();
		if ((options === null || options === void 0 ? void 0 : options.versionId) != null) query.set("versionId", String(options.versionId));
		const queryString = query.toString();
		return _this10.handleOperation(async () => {
			return recursiveToCamel(await get(_this10.fetch, `${_this10.url}/object/info/${_path}${queryString ? `?${queryString}` : ""}`, { headers: _this10.headers }));
		});
	}
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
	async exists(path) {
		var _this11 = this;
		const _path = _this11._getFinalPath(path);
		try {
			await head(_this11.fetch, `${_this11.url}/object/${_path}`, { headers: _this11.headers });
			return {
				data: true,
				error: null
			};
		} catch (error) {
			if (_this11.shouldThrowOnError) throw error;
			if (isStorageError(error)) {
				var _error$originalError;
				const status = error instanceof StorageApiError ? error.status : error instanceof StorageUnknownError ? (_error$originalError = error.originalError) === null || _error$originalError === void 0 ? void 0 : _error$originalError.status : void 0;
				if (status !== void 0 && [400, 404].includes(status)) return {
					data: false,
					error
				};
			}
			throw error;
		}
	}
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
	getPublicUrl(path, options) {
		const _path = this._getFinalPath(path);
		const query = new URLSearchParams();
		if (options === null || options === void 0 ? void 0 : options.download) query.set("download", options.download === true ? "" : options.download);
		if (options === null || options === void 0 ? void 0 : options.transform) this.applyTransformOptsToQuery(query, options.transform);
		if ((options === null || options === void 0 ? void 0 : options.cacheNonce) != null) query.set("cacheNonce", String(options.cacheNonce));
		if ((options === null || options === void 0 ? void 0 : options.versionId) != null) query.set("versionId", String(options.versionId));
		const queryString = query.toString();
		const renderPath = typeof (options === null || options === void 0 ? void 0 : options.transform) === "object" && options.transform !== null && Object.keys(options.transform).length > 0 ? "render/image" : "object";
		return { data: { publicUrl: encodeURI(`${this.url}/${renderPath}/public/${_path}`) + (queryString ? `?${queryString}` : "") } };
	}
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
	async remove(paths) {
		var _this12 = this;
		return _this12.handleOperation(async () => {
			return await remove(_this12.fetch, `${_this12.url}/object/${_this12.bucketId}`, { prefixes: paths }, { headers: _this12.headers });
		});
	}
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
	async purgeCache(path, options, parameters) {
		var _this13 = this;
		return _this13.handleOperation(async () => {
			const _path = encodeStoragePath(_this13._getFinalPath(path));
			const query = new URLSearchParams();
			if (options === null || options === void 0 ? void 0 : options.transformations) query.set("transformations", "true");
			const queryString = query.toString();
			return await remove(_this13.fetch, `${_this13.url}/cdn/${_path}${queryString ? `?${queryString}` : ""}`, {}, { headers: _this13.headers }, parameters);
		});
	}
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
	async list(path, options, parameters) {
		var _this14 = this;
		return _this14.handleOperation(async () => {
			const sortBy = (options === null || options === void 0 ? void 0 : options.sortBy) ? _objectSpread2(_objectSpread2({}, DEFAULT_SEARCH_OPTIONS.sortBy), options.sortBy) : DEFAULT_SEARCH_OPTIONS.sortBy;
			const body = _objectSpread2(_objectSpread2(_objectSpread2({}, DEFAULT_SEARCH_OPTIONS), options), {}, {
				sortBy,
				prefix: path || ""
			});
			return await post(_this14.fetch, `${_this14.url}/object/list/${_this14.bucketId}`, body, { headers: _this14.headers }, parameters);
		});
	}
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
	async listV2(options, parameters) {
		var _this15 = this;
		return _this15.handleOperation(async () => {
			const body = _objectSpread2({}, options);
			return await post(_this15.fetch, `${_this15.url}/object/list-v2/${_this15.bucketId}`, body, { headers: _this15.headers }, parameters);
		});
	}
	encodeMetadata(metadata) {
		return JSON.stringify(metadata);
	}
	toBase64(data) {
		if (typeof Buffer !== "undefined") return Buffer.from(data).toString("base64");
		return btoa(data);
	}
	_getFinalPath(path) {
		return `${this.bucketId}/${path.replace(/^\/+/, "")}`;
	}
	_removeEmptyFolders(path) {
		return path.replace(/^\/|\/$/g, "").replace(/\/+/g, "/");
	}
	/** Modifies the `query`, appending values the from `transform` */
	applyTransformOptsToQuery(query, transform) {
		if (transform.width) query.set("width", transform.width.toString());
		if (transform.height) query.set("height", transform.height.toString());
		if (transform.resize) query.set("resize", transform.resize);
		if (transform.format) query.set("format", transform.format);
		if (transform.quality) query.set("quality", transform.quality.toString());
		return query;
	}
};

//#endregion
//#region src/lib/version.ts
const version = "2.116.0";

//#endregion
//#region src/lib/constants.ts
const DEFAULT_HEADERS = { "X-Client-Info": `storage-js/${version}` };

//#endregion
//#region src/packages/StorageBucketApi.ts
var StorageBucketApi = class extends BaseApiClient {
	constructor(url, headers = {}, fetch$1, opts) {
		const baseUrl = new URL(url);
		if (opts === null || opts === void 0 ? void 0 : opts.useNewHostname) {
			if (/supabase\.(co|in|red)$/.test(baseUrl.hostname) && !baseUrl.hostname.includes("storage.supabase.")) baseUrl.hostname = baseUrl.hostname.replace("supabase.", "storage.supabase.");
		}
		const finalUrl = baseUrl.href.replace(/\/$/, "");
		const finalHeaders = _objectSpread2(_objectSpread2({}, DEFAULT_HEADERS), headers);
		super(finalUrl, finalHeaders, fetch$1, "storage");
	}
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
	async listBuckets(options) {
		var _this = this;
		return _this.handleOperation(async () => {
			const queryString = _this.listBucketOptionsToQueryString(options);
			return await get(_this.fetch, `${_this.url}/bucket${queryString}`, { headers: _this.headers });
		});
	}
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
	async getBucket(id) {
		var _this2 = this;
		return _this2.handleOperation(async () => {
			return await get(_this2.fetch, `${_this2.url}/bucket/${id}`, { headers: _this2.headers });
		});
	}
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
	async createBucket(id, options = { public: false }) {
		var _this3 = this;
		return _this3.handleOperation(async () => {
			return await post(_this3.fetch, `${_this3.url}/bucket`, {
				id,
				name: id,
				type: options.type,
				public: options.public,
				file_size_limit: options.fileSizeLimit,
				allowed_mime_types: options.allowedMimeTypes,
				versioning_status: options.versioningStatus
			}, { headers: _this3.headers });
		});
	}
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
	async updateBucket(id, options) {
		var _this4 = this;
		return _this4.handleOperation(async () => {
			return await put(_this4.fetch, `${_this4.url}/bucket/${id}`, {
				id,
				name: id,
				public: options.public,
				file_size_limit: options.fileSizeLimit,
				allowed_mime_types: options.allowedMimeTypes,
				versioning_status: options.versioningStatus
			}, { headers: _this4.headers });
		});
	}
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
	async emptyBucket(id) {
		var _this5 = this;
		return _this5.handleOperation(async () => {
			return await post(_this5.fetch, `${_this5.url}/bucket/${id}/empty`, {}, { headers: _this5.headers });
		});
	}
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
	async deleteBucket(id) {
		var _this6 = this;
		return _this6.handleOperation(async () => {
			return await remove(_this6.fetch, `${_this6.url}/bucket/${id}`, {}, { headers: _this6.headers });
		});
	}
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
	async getBucketLifecycle(id) {
		var _this7 = this;
		return _this7.handleOperation(async () => {
			return await get(_this7.fetch, _this7.bucketLifecycleUrl(id), { headers: _this7.headers });
		});
	}
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
	async updateBucketLifecycle(id, configuration) {
		var _this8 = this;
		return _this8.handleOperation(async () => {
			return await put(_this8.fetch, _this8.bucketLifecycleUrl(id), configuration, { headers: _this8.headers });
		});
	}
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
	async deleteBucketLifecycle(id) {
		var _this9 = this;
		return _this9.handleOperation(async () => {
			return await remove(_this9.fetch, _this9.bucketLifecycleUrl(id), {}, { headers: _this9.headers });
		});
	}
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
	async purgeBucketCache(id, options, parameters) {
		var _this10 = this;
		return _this10.handleOperation(async () => {
			const query = new URLSearchParams();
			if (options === null || options === void 0 ? void 0 : options.transformations) query.set("transformations", "true");
			const queryString = query.toString();
			return await remove(_this10.fetch, `${_this10.url}/cdn/${encodeStoragePath(id)}${queryString ? `?${queryString}` : ""}`, {}, { headers: _this10.headers }, parameters);
		});
	}
	bucketLifecycleUrl(id) {
		return `${this.url}/bucket/${encodeStoragePath(id)}/lifecycle`;
	}
	listBucketOptionsToQueryString(options) {
		const params = {};
		if (options) {
			if ("limit" in options) params.limit = String(options.limit);
			if ("offset" in options) params.offset = String(options.offset);
			if (options.search) params.search = options.search;
			if (options.sortColumn) params.sortColumn = options.sortColumn;
			if (options.sortOrder) params.sortOrder = options.sortOrder;
		}
		return Object.keys(params).length > 0 ? "?" + new URLSearchParams(params).toString() : "";
	}
};

//#endregion
//#region src/packages/StorageAnalyticsClient.ts
/**
* Client class for managing Analytics Buckets using Iceberg tables
* Provides methods for creating, listing, and deleting analytics buckets
*/
var StorageAnalyticsClient = class extends BaseApiClient {
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
	constructor(url, headers = {}, fetch$1) {
		const finalUrl = url.replace(/\/$/, "");
		const finalHeaders = _objectSpread2(_objectSpread2({}, DEFAULT_HEADERS), headers);
		super(finalUrl, finalHeaders, fetch$1, "storage");
	}
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
	async createBucket(name) {
		var _this = this;
		return _this.handleOperation(async () => {
			return await post(_this.fetch, `${_this.url}/bucket`, { name }, { headers: _this.headers });
		});
	}
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
	async listBuckets(options) {
		var _this2 = this;
		return _this2.handleOperation(async () => {
			const queryParams = new URLSearchParams();
			if ((options === null || options === void 0 ? void 0 : options.limit) !== void 0) queryParams.set("limit", options.limit.toString());
			if ((options === null || options === void 0 ? void 0 : options.offset) !== void 0) queryParams.set("offset", options.offset.toString());
			if (options === null || options === void 0 ? void 0 : options.sortColumn) queryParams.set("sortColumn", options.sortColumn);
			if (options === null || options === void 0 ? void 0 : options.sortOrder) queryParams.set("sortOrder", options.sortOrder);
			if (options === null || options === void 0 ? void 0 : options.search) queryParams.set("search", options.search);
			const queryString = queryParams.toString();
			const url = queryString ? `${_this2.url}/bucket?${queryString}` : `${_this2.url}/bucket`;
			return await get(_this2.fetch, url, { headers: _this2.headers });
		});
	}
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
	async deleteBucket(bucketName) {
		var _this3 = this;
		return _this3.handleOperation(async () => {
			return await remove(_this3.fetch, `${_this3.url}/bucket/${bucketName}`, {}, { headers: _this3.headers });
		});
	}
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
	from(bucketName) {
		var _this4 = this;
		if (!isValidBucketName(bucketName)) throw new StorageError("Invalid bucket name: File, folder, and bucket names must follow AWS object key naming guidelines and should avoid the use of any other characters.");
		const catalog = new IcebergRestCatalog({
			baseUrl: this.url,
			catalogName: bucketName,
			auth: {
				type: "custom",
				getHeaders: async () => _this4.headers
			},
			fetch: this.fetch
		});
		const shouldThrowOnError = this.shouldThrowOnError;
		return new Proxy(catalog, { get(target, prop) {
			const value = target[prop];
			if (typeof value !== "function") return value;
			return async (...args) => {
				try {
					return {
						data: await value.apply(target, args),
						error: null
					};
				} catch (error) {
					if (shouldThrowOnError) throw error;
					return {
						data: null,
						error
					};
				}
			};
		} });
	}
};

//#endregion
//#region src/packages/VectorIndexApi.ts
/**
* @hidden
* Base implementation for vector index operations.
* Use {@link VectorBucketScope} via `supabase.storage.vectors.from('bucket')` instead.
*/
var VectorIndexApi = class extends BaseApiClient {
	/** Creates a new VectorIndexApi instance */
	constructor(url, headers = {}, fetch$1) {
		const finalUrl = url.replace(/\/$/, "");
		const finalHeaders = _objectSpread2(_objectSpread2({}, DEFAULT_HEADERS), {}, { "Content-Type": "application/json" }, headers);
		super(finalUrl, finalHeaders, fetch$1, "vectors");
	}
	/** Creates a new vector index within a bucket */
	async createIndex(options) {
		var _this = this;
		return _this.handleOperation(async () => {
			return await vectorsApi.post(_this.fetch, `${_this.url}/CreateIndex`, options, { headers: _this.headers }) || {};
		});
	}
	/** Retrieves metadata for a specific vector index */
	async getIndex(vectorBucketName, indexName) {
		var _this2 = this;
		return _this2.handleOperation(async () => {
			return await vectorsApi.post(_this2.fetch, `${_this2.url}/GetIndex`, {
				vectorBucketName,
				indexName
			}, { headers: _this2.headers });
		});
	}
	/** Lists vector indexes within a bucket with optional filtering and pagination */
	async listIndexes(options) {
		var _this3 = this;
		return _this3.handleOperation(async () => {
			return await vectorsApi.post(_this3.fetch, `${_this3.url}/ListIndexes`, options, { headers: _this3.headers });
		});
	}
	/** Deletes a vector index and all its data */
	async deleteIndex(vectorBucketName, indexName) {
		var _this4 = this;
		return _this4.handleOperation(async () => {
			return await vectorsApi.post(_this4.fetch, `${_this4.url}/DeleteIndex`, {
				vectorBucketName,
				indexName
			}, { headers: _this4.headers }) || {};
		});
	}
};

//#endregion
//#region src/packages/VectorDataApi.ts
/**
* @hidden
* Base implementation for vector data operations.
* Use {@link VectorIndexScope} via `supabase.storage.vectors.from('bucket').index('idx')` instead.
*/
var VectorDataApi = class extends BaseApiClient {
	/** Creates a new VectorDataApi instance */
	constructor(url, headers = {}, fetch$1) {
		const finalUrl = url.replace(/\/$/, "");
		const finalHeaders = _objectSpread2(_objectSpread2({}, DEFAULT_HEADERS), {}, { "Content-Type": "application/json" }, headers);
		super(finalUrl, finalHeaders, fetch$1, "vectors");
	}
	/** Inserts or updates vectors in batch (1-500 per request) */
	async putVectors(options) {
		var _this = this;
		if (options.vectors.length < 1 || options.vectors.length > 500) throw new Error("Vector batch size must be between 1 and 500 items");
		return _this.handleOperation(async () => {
			return await vectorsApi.post(_this.fetch, `${_this.url}/PutVectors`, options, { headers: _this.headers }) || {};
		});
	}
	/** Retrieves vectors by their keys in batch */
	async getVectors(options) {
		var _this2 = this;
		return _this2.handleOperation(async () => {
			return await vectorsApi.post(_this2.fetch, `${_this2.url}/GetVectors`, options, { headers: _this2.headers });
		});
	}
	/** Lists vectors in an index with pagination */
	async listVectors(options) {
		var _this3 = this;
		if (options.segmentCount !== void 0) {
			if (options.segmentCount < 1 || options.segmentCount > 16) throw new Error("segmentCount must be between 1 and 16");
			if (options.segmentIndex !== void 0) {
				if (options.segmentIndex < 0 || options.segmentIndex >= options.segmentCount) throw new Error(`segmentIndex must be between 0 and ${options.segmentCount - 1}`);
			}
		}
		return _this3.handleOperation(async () => {
			return await vectorsApi.post(_this3.fetch, `${_this3.url}/ListVectors`, options, { headers: _this3.headers });
		});
	}
	/** Queries for similar vectors using approximate nearest neighbor search */
	async queryVectors(options) {
		var _this4 = this;
		return _this4.handleOperation(async () => {
			return await vectorsApi.post(_this4.fetch, `${_this4.url}/QueryVectors`, options, { headers: _this4.headers });
		});
	}
	/** Deletes vectors by their keys in batch (1-500 per request) */
	async deleteVectors(options) {
		var _this5 = this;
		if (options.keys.length < 1 || options.keys.length > 500) throw new Error("Keys batch size must be between 1 and 500 items");
		return _this5.handleOperation(async () => {
			return await vectorsApi.post(_this5.fetch, `${_this5.url}/DeleteVectors`, options, { headers: _this5.headers }) || {};
		});
	}
};

//#endregion
//#region src/packages/VectorBucketApi.ts
/**
* @hidden
* Base implementation for vector bucket operations.
* Use {@link StorageVectorsClient} via `supabase.storage.vectors` instead.
*/
var VectorBucketApi = class extends BaseApiClient {
	/** Creates a new VectorBucketApi instance */
	constructor(url, headers = {}, fetch$1) {
		const finalUrl = url.replace(/\/$/, "");
		const finalHeaders = _objectSpread2(_objectSpread2({}, DEFAULT_HEADERS), {}, { "Content-Type": "application/json" }, headers);
		super(finalUrl, finalHeaders, fetch$1, "vectors");
	}
	/** Creates a new vector bucket */
	async createBucket(vectorBucketName) {
		var _this = this;
		return _this.handleOperation(async () => {
			return await vectorsApi.post(_this.fetch, `${_this.url}/CreateVectorBucket`, { vectorBucketName }, { headers: _this.headers }) || {};
		});
	}
	/** Retrieves metadata for a specific vector bucket */
	async getBucket(vectorBucketName) {
		var _this2 = this;
		return _this2.handleOperation(async () => {
			return await vectorsApi.post(_this2.fetch, `${_this2.url}/GetVectorBucket`, { vectorBucketName }, { headers: _this2.headers });
		});
	}
	/** Lists vector buckets with optional filtering and pagination */
	async listBuckets(options = {}) {
		var _this3 = this;
		return _this3.handleOperation(async () => {
			return await vectorsApi.post(_this3.fetch, `${_this3.url}/ListVectorBuckets`, options, { headers: _this3.headers });
		});
	}
	/** Deletes a vector bucket (must be empty first) */
	async deleteBucket(vectorBucketName) {
		var _this4 = this;
		return _this4.handleOperation(async () => {
			return await vectorsApi.post(_this4.fetch, `${_this4.url}/DeleteVectorBucket`, { vectorBucketName }, { headers: _this4.headers }) || {};
		});
	}
};

//#endregion
//#region src/packages/StorageVectorsClient.ts
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
var StorageVectorsClient = class extends VectorBucketApi {
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
	constructor(url, options = {}) {
		super(url, options.headers || {}, options.fetch);
	}
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
	from(vectorBucketName) {
		return new VectorBucketScope(this.url, this.headers, vectorBucketName, this.fetch);
	}
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
	async createBucket(vectorBucketName) {
		var _superprop_getCreateBucket = () => super.createBucket, _this = this;
		return _superprop_getCreateBucket().call(_this, vectorBucketName);
	}
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
	async getBucket(vectorBucketName) {
		var _superprop_getGetBucket = () => super.getBucket, _this2 = this;
		return _superprop_getGetBucket().call(_this2, vectorBucketName);
	}
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
	async listBuckets(options = {}) {
		var _superprop_getListBuckets = () => super.listBuckets, _this3 = this;
		return _superprop_getListBuckets().call(_this3, options);
	}
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
	async deleteBucket(vectorBucketName) {
		var _superprop_getDeleteBucket = () => super.deleteBucket, _this4 = this;
		return _superprop_getDeleteBucket().call(_this4, vectorBucketName);
	}
};
/**
*
* @alpha
*
* Scoped client for operations within a specific vector bucket
* Provides index management and access to vector operations
*
* **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
*/
var VectorBucketScope = class extends VectorIndexApi {
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
	constructor(url, headers, vectorBucketName, fetch$1) {
		super(url, headers, fetch$1);
		this.vectorBucketName = vectorBucketName;
	}
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
	async createIndex(options) {
		var _superprop_getCreateIndex = () => super.createIndex, _this5 = this;
		return _superprop_getCreateIndex().call(_this5, _objectSpread2(_objectSpread2({}, options), {}, { vectorBucketName: _this5.vectorBucketName }));
	}
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
	async listIndexes(options = {}) {
		var _superprop_getListIndexes = () => super.listIndexes, _this6 = this;
		return _superprop_getListIndexes().call(_this6, _objectSpread2(_objectSpread2({}, options), {}, { vectorBucketName: _this6.vectorBucketName }));
	}
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
	async getIndex(indexName) {
		var _superprop_getGetIndex = () => super.getIndex, _this7 = this;
		return _superprop_getGetIndex().call(_this7, _this7.vectorBucketName, indexName);
	}
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
	async deleteIndex(indexName) {
		var _superprop_getDeleteIndex = () => super.deleteIndex, _this8 = this;
		return _superprop_getDeleteIndex().call(_this8, _this8.vectorBucketName, indexName);
	}
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
	index(indexName) {
		return new VectorIndexScope(this.url, this.headers, this.vectorBucketName, indexName, this.fetch);
	}
};
/**
*
* @alpha
*
* Scoped client for operations within a specific vector index
* Provides vector data operations (put, get, list, query, delete)
*
* **Public alpha:** This API is part of a public alpha release and may not be available to your account type.
*/
var VectorIndexScope = class extends VectorDataApi {
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
	constructor(url, headers, vectorBucketName, indexName, fetch$1) {
		super(url, headers, fetch$1);
		this.vectorBucketName = vectorBucketName;
		this.indexName = indexName;
	}
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
	async putVectors(options) {
		var _superprop_getPutVectors = () => super.putVectors, _this9 = this;
		return _superprop_getPutVectors().call(_this9, _objectSpread2(_objectSpread2({}, options), {}, {
			vectorBucketName: _this9.vectorBucketName,
			indexName: _this9.indexName
		}));
	}
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
	async getVectors(options) {
		var _superprop_getGetVectors = () => super.getVectors, _this10 = this;
		return _superprop_getGetVectors().call(_this10, _objectSpread2(_objectSpread2({}, options), {}, {
			vectorBucketName: _this10.vectorBucketName,
			indexName: _this10.indexName
		}));
	}
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
	async listVectors(options = {}) {
		var _superprop_getListVectors = () => super.listVectors, _this11 = this;
		return _superprop_getListVectors().call(_this11, _objectSpread2(_objectSpread2({}, options), {}, {
			vectorBucketName: _this11.vectorBucketName,
			indexName: _this11.indexName
		}));
	}
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
	async queryVectors(options) {
		var _superprop_getQueryVectors = () => super.queryVectors, _this12 = this;
		return _superprop_getQueryVectors().call(_this12, _objectSpread2(_objectSpread2({}, options), {}, {
			vectorBucketName: _this12.vectorBucketName,
			indexName: _this12.indexName
		}));
	}
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
	async deleteVectors(options) {
		var _superprop_getDeleteVectors = () => super.deleteVectors, _this13 = this;
		return _superprop_getDeleteVectors().call(_this13, _objectSpread2(_objectSpread2({}, options), {}, {
			vectorBucketName: _this13.vectorBucketName,
			indexName: _this13.indexName
		}));
	}
};

//#endregion
//#region src/StorageClient.ts
var StorageClient = class extends StorageBucketApi {
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
	constructor(url, headers = {}, fetch$1, opts) {
		super(url, headers, fetch$1, opts);
	}
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
	from(id) {
		return new StorageFileApi(this.url, this.headers, id, this.fetch);
	}
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
	get vectors() {
		return new StorageVectorsClient(this.url + "/vector", {
			headers: this.headers,
			fetch: this.fetch
		});
	}
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
	get analytics() {
		return new StorageAnalyticsClient(this.url + "/iceberg", this.headers, this.fetch);
	}
};

//#endregion
export { StorageAnalyticsClient, StorageApiError, StorageClient, StorageError, StorageUnknownError, StorageVectorsApiError, StorageVectorsClient, StorageVectorsError, StorageVectorsErrorCode, StorageVectorsUnknownError, VectorBucketApi, VectorBucketScope, VectorDataApi, VectorIndexApi, VectorIndexScope, isStorageError, isStorageVectorsError };
//# sourceMappingURL=index.mjs.map