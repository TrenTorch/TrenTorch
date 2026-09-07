# iceberg-js

[![CI](https://github.com/supabase/iceberg-js/actions/workflows/ci.yml/badge.svg)](https://github.com/supabase/iceberg-js/actions/workflows/ci.yml)
[![npm version](https://badge.fury.io/js/iceberg-js.svg)](https://www.npmjs.com/package/iceberg-js)
[![pkg.pr.new](https://pkg.pr.new/badge/supabase/iceberg-js)](https://pkg.pr.new/~/supabase/iceberg-js)

A small, framework-agnostic JavaScript/TypeScript client for the **Apache Iceberg REST Catalog**.

## Features

- **Generic**: Works with any Iceberg REST Catalog implementation, not tied to any specific vendor
- **Minimal**: Thin HTTP wrapper over the official REST API, no engine-specific logic
- **Type-safe**: First-class TypeScript support with strongly-typed request/response models
- **Fetch-based**: Uses native `fetch` API with support for custom implementations
- **Universal**: Targets Node 20+ and modern browsers (ES2020)
- **Catalog-only**: Focused on catalog operations (no data reading/Parquet support in v0.1.0)

## Documentation

📚 **Full API documentation**: [supabase.github.io/iceberg-js](https://supabase.github.io/iceberg-js/)

## Installation

```bash
npm install iceberg-js
```

## Quick Start

```typescript
import { IcebergRestCatalog } from 'iceberg-js'

const catalog = new IcebergRestCatalog({
  baseUrl: 'https://my-catalog.example.com/iceberg/v1',
  auth: {
    type: 'bearer',
    token: process.env.ICEBERG_TOKEN,
  },
})

// Create a namespace
await catalog.createNamespace({ namespace: ['analytics'] })

// Create a table
await catalog.createTable(
  { namespace: ['analytics'] },
  {
    name: 'events',
    schema: {
      type: 'struct',
      fields: [
        { id: 1, name: 'id', type: 'long', required: true },
        { id: 2, name: 'timestamp', type: 'timestamp', required: true },
        { id: 3, name: 'user_id', type: 'string', required: false },
      ],
      'schema-id': 0,
      'identifier-field-ids': [1],
    },
    'partition-spec': {
      'spec-id': 0,
      fields: [],
    },
    'write-order': {
      'order-id': 0,
      fields: [],
    },
    properties: {
      'write.format.default': 'parquet',
    },
  }
)
```

## API Reference

### Constructor

#### `new IcebergRestCatalog(options)`

Creates a new catalog client instance.

**Options:**

- `baseUrl` (string, required): Base URL of the REST catalog
- `auth` (AuthConfig, optional): Authentication configuration
- `catalogName` (string, optional): Catalog name for multi-catalog servers. When specified, requests are sent to `{baseUrl}/v1/{catalogName}/...`. For example, with `baseUrl: 'https://host.com'` and `catalogName: 'prod'`, requests go to `https://host.com/v1/prod/namespaces`
- `fetch` (typeof fetch, optional): Custom fetch implementation
- `accessDelegation` (AccessDelegation[], optional): Access delegation mechanisms to request from the server

**Authentication types:**

```typescript
// No authentication
{ type: 'none' }

// Bearer token
{ type: 'bearer', token: 'your-token' }

// Custom header
{ type: 'header', name: 'X-Custom-Auth', value: 'secret' }

// Custom function
{ type: 'custom', getHeaders: async () => ({ 'Authorization': 'Bearer ...' }) }
```

**Access Delegation:**

Access delegation allows the catalog server to provide temporary credentials or sign requests on your behalf:

```typescript
import { IcebergRestCatalog } from 'iceberg-js'

const catalog = new IcebergRestCatalog({
  baseUrl: 'https://catalog.example.com/iceberg/v1',
  auth: { type: 'bearer', token: 'your-token' },
  // Request vended credentials for data access
  accessDelegation: ['vended-credentials'],
})

// The server may return temporary credentials in the table metadata
const metadata = await catalog.loadTable({ namespace: ['analytics'], name: 'events' })
// Use credentials from metadata.config to access table data files
```

Supported delegation mechanisms:

- `vended-credentials`: Server provides temporary credentials (e.g., AWS STS tokens) for accessing table data
- `remote-signing`: Server signs data access requests on behalf of the client

### Namespace Operations

#### `listNamespaces(parent?: NamespaceIdentifier): Promise<NamespaceIdentifier[]>`

List all namespaces, optionally under a parent namespace.

```typescript
const namespaces = await catalog.listNamespaces()
// [{ namespace: ['default'] }, { namespace: ['analytics'] }]

const children = await catalog.listNamespaces({ namespace: ['analytics'] })
// [{ namespace: ['analytics', 'prod'] }]
```

#### `createNamespace(id: NamespaceIdentifier, metadata?: NamespaceMetadata): Promise<void>`

Create a new namespace with optional properties.

```typescript
await catalog.createNamespace({ namespace: ['analytics'] }, { properties: { owner: 'data-team' } })
```

#### `dropNamespace(id: NamespaceIdentifier): Promise<void>`

Drop a namespace. The namespace must be empty.

```typescript
await catalog.dropNamespace({ namespace: ['analytics'] })
```

#### `loadNamespaceMetadata(id: NamespaceIdentifier): Promise<NamespaceMetadata>`

Load namespace metadata and properties.

```typescript
const metadata = await catalog.loadNamespaceMetadata({ namespace: ['analytics'] })
// { properties: { owner: 'data-team', ... } }
```

### Table Operations

#### `listTables(namespace: NamespaceIdentifier): Promise<TableIdentifier[]>`

List all tables in a namespace.

```typescript
const tables = await catalog.listTables({ namespace: ['analytics'] })
// [{ namespace: ['analytics'], name: 'events' }]
```

#### `createTable(namespace: NamespaceIdentifier, request: CreateTableRequest): Promise<TableMetadata>`

Create a new table.

```typescript
const metadata = await catalog.createTable(
  { namespace: ['analytics'] },
  {
    name: 'events',
    schema: {
      type: 'struct',
      fields: [
        { id: 1, name: 'id', type: 'long', required: true },
        { id: 2, name: 'timestamp', type: 'timestamp', required: true },
      ],
      'schema-id': 0,
    },
    'partition-spec': {
      'spec-id': 0,
      fields: [
        {
          source_id: 2,
          field_id: 1000,
          name: 'ts_day',
          transform: 'day',
        },
      ],
    },
  }
)
```

#### `loadTable(id: TableIdentifier): Promise<TableMetadata>`

Load table metadata.

```typescript
const metadata = await catalog.loadTable({
  namespace: ['analytics'],
  name: 'events',
})
```

#### `updateTable(id: TableIdentifier, request: UpdateTableRequest): Promise<TableMetadata>`

Update table metadata (schema, partition spec, or properties).

```typescript
const updated = await catalog.updateTable(
  { namespace: ['analytics'], name: 'events' },
  {
    properties: { 'read.split.target-size': '134217728' },
  }
)
```

#### `dropTable(id: TableIdentifier): Promise<void>`

Drop a table from the catalog.

```typescript
await catalog.dropTable({ namespace: ['analytics'], name: 'events' })
```

## Error Handling

All API errors throw an `IcebergError` with details from the server:

```typescript
import { IcebergError } from 'iceberg-js'

try {
  await catalog.loadTable({ namespace: ['test'], name: 'missing' })
} catch (error) {
  if (error instanceof IcebergError) {
    console.log(error.status) // 404
    console.log(error.icebergType) // 'NoSuchTableException'
    console.log(error.message) // 'Table does not exist'
  }
}
```

## TypeScript Types

The library exports all relevant types:

```typescript
import type {
  NamespaceIdentifier,
  TableIdentifier,
  TableSchema,
  TableField,
  IcebergType,
  PartitionSpec,
  SortOrder,
  CreateTableRequest,
  TableMetadata,
  AuthConfig,
  AccessDelegation,
} from 'iceberg-js'
```

## Supported Iceberg Types

The following Iceberg primitive types are supported:

- `boolean`, `int`, `long`, `float`, `double`
- `string`, `uuid`, `binary`
- `date`, `time`, `timestamp`, `timestamptz`
- `decimal(precision, scale)`, `fixed(length)`

## Compatibility

This package is built to work in **all** Node.js and JavaScript environments:

| Environment         | Module System        | Import Method                           | Status                |
| ------------------- | -------------------- | --------------------------------------- | --------------------- |
| Node.js ESM         | `"type": "module"`   | `import { ... } from 'iceberg-js'`      | ✅ Fully supported    |
| Node.js CommonJS    | Default              | `const { ... } = require('iceberg-js')` | ✅ Fully supported    |
| TypeScript ESM      | `module: "ESNext"`   | `import { ... } from 'iceberg-js'`      | ✅ Full type support  |
| TypeScript CommonJS | `module: "CommonJS"` | `import { ... } from 'iceberg-js'`      | ✅ Full type support  |
| Bundlers            | Any                  | Webpack, Vite, esbuild, Rollup, etc.    | ✅ Auto-detected      |
| Browsers            | ESM                  | `<script type="module">`                | ✅ Modern browsers    |
| Deno                | ESM                  | `import` from npm:                      | ✅ With npm specifier |

**Package exports:**

- ESM: `dist/index.mjs` with `dist/index.d.ts`
- CommonJS: `dist/index.cjs` with `dist/index.d.cts`
- Proper `exports` field for Node.js 12+ module resolution

All scenarios are tested in CI on Node.js 20 and 22.

## Browser Usage

The library works in modern browsers that support native `fetch`:

```typescript
import { IcebergRestCatalog } from 'iceberg-js'

const catalog = new IcebergRestCatalog({
  baseUrl: 'https://public-catalog.example.com/iceberg/v1',
  auth: { type: 'none' },
})

const namespaces = await catalog.listNamespaces()
```

## Node.js Usage

Node.js 20+ includes native `fetch` support. For older versions, provide a custom fetch implementation:

```typescript
import { IcebergRestCatalog } from 'iceberg-js'
import fetch from 'node-fetch'

const catalog = new IcebergRestCatalog({
  baseUrl: 'https://catalog.example.com/iceberg/v1',
  auth: { type: 'bearer', token: 'token' },
  fetch: fetch as any,
})
```

## Limitations (v0.1.0)

This is a catalog client only. The following are **not supported**:

- Reading table data (scanning Parquet files)
- Writing data to tables
- Advanced table operations (commits, snapshots, time travel)
- Views support
- Multi-table transactions

## Development

```bash
# Install dependencies
pnpm install

# Build the library
pnpm run build

# Run unit tests
pnpm test

# Run integration tests (requires Docker)
pnpm test:integration

# Run integration tests with cleanup (for CI)
pnpm test:integration:ci

# Run compatibility tests (all module systems)
pnpm test:compatibility

# Format code
pnpm run format

# Lint and test
pnpm run check
```

### Testing with Docker

Integration tests run against a local Iceberg REST Catalog in Docker. See [TESTING-DOCKER.md](./test/integration/TESTING-DOCKER.md) for details.

```bash
# Start Docker services and run integration tests
pnpm test:integration

# Or manually
docker compose up -d
npx tsx test/integration/test-local-catalog.ts
docker compose down -v
```

### Compatibility Testing

The `test:compatibility` script verifies the package works correctly in all JavaScript/TypeScript environments:

- **Pure JavaScript ESM** - Projects with `"type": "module"`
- **Pure JavaScript CommonJS** - Traditional Node.js projects
- **TypeScript ESM** - TypeScript with `module: "ESNext"`
- **TypeScript CommonJS** - TypeScript with `module: "CommonJS"`

These tests ensure proper module resolution, type definitions, and runtime behavior across all supported environments. See [test/compatibility/README.md](./test/compatibility/README.md) for more details.

## License

MIT

## Releases

This project uses [release-please](https://github.com/googleapis/release-please) for automated releases. Here's how it works:

1. **Commit with conventional commits**: Use [Conventional Commits](https://www.conventionalcommits.org/) format for your commits:
   - `feat:` for new features (minor version bump)
   - `fix:` for bug fixes (patch version bump)
   - `feat!:` or `BREAKING CHANGE:` for breaking changes (major version bump)
   - `chore:`, `docs:`, `test:`, etc. for non-release commits

2. **Release PR is created automatically**: When you push to `main`, release-please creates/updates a release PR with:
   - Version bump in `package.json`
   - Updated `CHANGELOG.md`
   - Release notes

3. **Merge the release PR**: When you're ready to release, merge the PR. This will:
   - Create a GitHub release and git tag
   - Automatically publish to npm with provenance (using trusted publishing, no secrets needed)

**Example commits:**

```bash
git commit -m "feat: add support for view operations"
git commit -m "fix: handle empty namespace list correctly"
git commit -m "feat!: change auth config structure"
```

## Contributing

Contributions are welcome! This library aims to be a minimal, generic client for the Iceberg REST Catalog API.
