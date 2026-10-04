# Implementation Plan: Add 120+ Deep-ML Questions to TrenTorch

**Goal:** Build and integrate 120+ questions from Deep-ML across 6 topic areas, adding 11 new subsections to TrenTorch tracks with full IDE testing support.

**Architecture:**

- SQL: Mock SQL executor in Node.js backend (returns parsed results without a real DB)
- ML Compilers: Code interpretation + visual explanation tasks (no CUDA, pure Python/concepts)
- DSA: Classical algorithm problems with input/output verification
- Inference: Performance calculation and cost analysis (numeric, no GPU)
- Distributed Training: Conceptual questions and mini-simulations in NumPy
- Performance Optimization: Numeric analysis and measurement-based questions

**Tech Stack:**

- Node.js mock SQL executor (SQL parser + in-memory data simulation)
- Python 3.14 for all question implementations
- Pytest for test validation
- SvelteKit prerendering (no API changes needed)

---

## Phase 1: Infrastructure & Templates (Days 1-2)

### Task 1.1: Create SQL Mock Executor

**Files:**

- Create: `src/lib/services/sqlExecutor.ts`
- Create: `src/lib/services/sqlDatasets.ts`
- Test: Verify 3 basic queries parse and return correct results

**Steps:**

1. Write failing test file `src/lib/services/__tests__/sqlExecutor.test.ts`:

```typescript
import { executeSql } from '../sqlExecutor';

describe('SQL Executor', () => {
	test('SELECT * returns all rows', () => {
		const result = executeSql('SELECT * FROM users');
		expect(result.rows.length).toBe(5);
		expect(result.rows[0]).toHaveProperty('id');
	});

	test('SELECT with WHERE filters rows', () => {
		const result = executeSql('SELECT * FROM users WHERE age > 25');
		expect(result.rows.length).toBe(2);
	});

	test('SELECT COUNT groups and aggregates', () => {
		const result = executeSql(
			'SELECT department, COUNT(*) as count FROM employees GROUP BY department'
		);
		expect(result.rows[0]).toHaveProperty('count');
	});
});
```

2. Run test (confirm all fail):

```bash
cd D:/KC/TrenTorch/TrenTorch_Web && npm test -- sqlExecutor.test.ts
```

3. Implement `src/lib/services/sqlExecutor.ts`:

```typescript
import { parseSQL } from './sqlParser';
import { getDataset } from './sqlDatasets';

export interface SQLResult {
	rows: Record<string, any>[];
	columns: string[];
	error?: string;
}

export function executeSql(query: string): SQLResult {
	try {
		const parsed = parseSQL(query);
		const dataset = getDataset(parsed.table);

		if (!dataset) {
			return { rows: [], columns: [], error: `Table ${parsed.table} not found` };
		}

		let rows = [...dataset.data];

		// WHERE clause
		if (parsed.where) {
			rows = rows.filter((row) => evaluateCondition(row, parsed.where));
		}

		// GROUP BY with aggregates
		if (parsed.groupBy) {
			rows = groupAndAggregate(rows, parsed.groupBy, parsed.aggregates);
		}

		// SELECT columns
		const selectedRows = rows.map((row) => {
			const result: Record<string, any> = {};
			parsed.columns.forEach((col) => {
				result[col] = row[col];
			});
			return result;
		});

		// ORDER BY
		if (parsed.orderBy) {
			selectedRows.sort((a, b) => {
				const aVal = a[parsed.orderBy.column];
				const bVal = b[parsed.orderBy.column];
				return parsed.orderBy.desc ? bVal - aVal : aVal - bVal;
			});
		}

		// LIMIT
		if (parsed.limit) {
			selectedRows.splice(parsed.limit);
		}

		return {
			rows: selectedRows,
			columns: parsed.columns
		};
	} catch (err) {
		return {
			rows: [],
			columns: [],
			error: String(err)
		};
	}
}

function evaluateCondition(row: Record<string, any>, condition: any): boolean {
	// Simple condition evaluator (AND/OR/comparison operators)
	// Implementation depends on parsed condition structure
	return true; // placeholder - expand based on parsed structure
}

function groupAndAggregate(
	rows: any[],
	groupBy: string[],
	aggregates: Record<string, string>
): any[] {
	const groups = new Map<string, any[]>();

	rows.forEach((row) => {
		const key = groupBy.map((col) => row[col]).join('|');
		if (!groups.has(key)) groups.set(key, []);
		groups.get(key)!.push(row);
	});

	return Array.from(groups.entries()).map(([key, groupRows]) => {
		const result: Record<string, any> = {};
		groupBy.forEach((col, i) => {
			result[col] = groupRows[0][col];
		});

		// Compute aggregates
		Object.entries(aggregates).forEach(([alias, aggFunc]) => {
			const match = aggFunc.match(/(\w+)\((\w+)\)/);
			if (match) {
				const [, func, col] = match;
				result[alias] = computeAggregate(
					func,
					groupRows.map((r) => r[col])
				);
			}
		});

		return result;
	});
}

function computeAggregate(func: string, values: any[]): any {
	switch (func.toLowerCase()) {
		case 'count':
			return values.length;
		case 'sum':
			return values.reduce((a, b) => a + b, 0);
		case 'avg':
			return values.reduce((a, b) => a + b, 0) / values.length;
		case 'max':
			return Math.max(...values);
		case 'min':
			return Math.min(...values);
		default:
			return null;
	}
}
```

4. Create `src/lib/services/sqlDatasets.ts`:

```typescript
export const DATASETS: Record<string, { columns: string[]; data: any[] }> = {
	users: {
		columns: ['id', 'name', 'age', 'department'],
		data: [
			{ id: 1, name: 'Alice', age: 30, department: 'Engineering' },
			{ id: 2, name: 'Bob', age: 25, department: 'Sales' },
			{ id: 3, name: 'Charlie', age: 35, department: 'Engineering' },
			{ id: 4, name: 'Diana', age: 28, department: 'HR' },
			{ id: 5, name: 'Eve', age: 32, department: 'Sales' }
		]
	},
	employees: {
		columns: ['id', 'name', 'salary', 'department', 'manager_id'],
		data: [
			{ id: 1, name: 'Alice', salary: 100000, department: 'Engineering', manager_id: null },
			{ id: 2, name: 'Bob', salary: 80000, department: 'Engineering', manager_id: 1 },
			{ id: 3, name: 'Charlie', salary: 120000, department: 'Sales', manager_id: null },
			{ id: 4, name: 'Diana', salary: 90000, department: 'Sales', manager_id: 3 }
		]
	}
};

export function getDataset(name: string) {
	return DATASETS[name.toLowerCase()];
}
```

5. Run tests (confirm green):

```bash
npm test -- sqlExecutor.test.ts
```

6. Commit:

```bash
cd D:/KC/TrenTorch/TrenTorch_Web && git add src/lib/services/sql* && git commit -m "Add SQL mock executor and datasets for question IDE

Implement SQL query parser and executor with support for:
- SELECT with column filtering
- WHERE conditions (basic)
- GROUP BY with COUNT/SUM/AVG/MAX/MIN
- ORDER BY and LIMIT
- In-memory dataset simulation (users, employees tables)

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

### Task 1.2: Create Question Directory Structure & Template

**Files:**

- Create: `data/app_data/03-data-science/04-sql/meta.json`
- Create: `data/app_data/03-data-science/04-sql/01-basics/meta.json`
- Create: `data/app_data/05-deep-learning/07-ml-compilers/meta.json`
- Create: `data/app_data/03-data-science/05-dsa/meta.json`
- Create: `data/app_data/06-language-modelling-attention-llms/07-inference-optimization/meta.json`
- Create: `data/app_data/10-distributed-systems/02-distributed-training/meta.json`
- Create: `data/app_data/10-distributed-systems/03-performance-optimization/meta.json`

**Steps:**

1. Create all `meta.json` files:

`data/app_data/03-data-science/04-sql/meta.json`:

```json
{
	"title": "SQL & Databases"
}
```

`data/app_data/03-data-science/04-sql/01-basics/meta.json`:

```json
{
	"title": "SQL Fundamentals"
}
```

`data/app_data/03-data-science/04-sql/02-intermediate/meta.json`:

```json
{
	"title": "Joins & Aggregation"
}
```

`data/app_data/03-data-science/04-sql/03-advanced/meta.json`:

```json
{
	"title": "Window Functions & Advanced"
}
```

(Repeat similar structure for ML Compilers, DSA, Inference, Distributed Training, Performance Optimization)

2. Run curriculum build to verify structure:

```bash
cd D:/KC/TrenTorch/TrenTorch_Web && node processes/curriculum-build/build.mjs
# Should output: "Curriculum OK: 11 roots, XXX questions"
```

3. Commit:

```bash
git add data/app_data && git commit -m "Add directory structure for SQL, ML Compilers, DSA, Inference, Distributed Training, Performance Optimization

Create subsection hierarchy:
- 03-data-science/04-sql (3 subsections)
- 05-deep-learning/07-ml-compilers (1 section)
- 03-data-science/05-dsa (2 subsections)
- 06-language-modelling-attention-llms/07-inference-optimization (1 section)
- 10-distributed-systems/02-distributed-training (1 section)
- 10-distributed-systems/03-performance-optimization (1 section)

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Phase 2: SQL Questions (Days 3-5, 51 questions total)

### Task 2.1: Build SQL Basics (10 questions)

**Files to Create:**

- `data/app_data/03-data-science/04-sql/01-basics/01-select-all/` (README.md, starter.py, solution.py, tests.py)
- ... (9 more question directories)

Each question follows this structure:

**README.md:**

```markdown
---
name: db-sql-select-all
topics: ['SQL', 'Databases']
companies:
  names: ['Google', 'Amazon', 'Microsoft', 'Meta']
  roles: 'Data Engineer / Analytics interviews'
---

# SELECT All Rows

## Problem

Write a SQL query that retrieves all columns and rows from the `users` table.

**Expected output:** 5 rows with columns (id, name, age, department)

## Constraints

- Return all columns
- No filtering
- No sorting
```

**starter.py:**

```python
def solve_select_all():
    """
    Returns the SQL query to select all rows from users table.
    """
    query = ""  # TODO: write your SQL query here
    return query
```

**solution.py:**

```python
def solve_select_all():
    query = "SELECT * FROM users"
    return query
```

**tests.py:**

```python
import pytest
from solution import solve_select_all
from src.lib.services.sqlExecutor import executeSql

def test_select_all_returns_all_rows():
    query = solve_select_all()
    result = executeSql(query)
    assert len(result.rows) == 5
    assert 'id' in result.rows[0]
    assert 'name' in result.rows[0]

def test_select_all_has_correct_columns():
    query = solve_select_all()
    result = executeSql(query)
    expected_cols = {'id', 'name', 'age', 'department'}
    actual_cols = set(result.rows[0].keys())
    assert actual_cols == expected_cols
```

**Repeat for 9 more basic questions:**

1. Select specific columns
2. Filter rows with WHERE (simple comparison)
3. Sort results with ORDER BY (ascending)
4. Remove duplicates with DISTINCT
5. Top N with LIMIT
6. Count rows with COUNT(*)
7. Average with AVG()
8. Filter with multiple WHERE conditions (AND)
9. Filter with OR conditions
10. NULL value handling (IS NULL / IS NOT NULL)

**Steps:**

1. Create all 10 question directories with README.md + starter/solution/tests.py
2. Run tests locally:

```bash
cd data/app_data/03-data-science/04-sql/01-basics/01-select-all && python -m pytest tests.py -v
```

3. Verify all pass
4. Run prettier on data/curriculum:

```bash
npx prettier --check data/curriculum
```

5. Commit all 10 questions

---

### Task 2.2: Build SQL Joins & Aggregation (20 questions)

**Questions (sampled):**

- Your first JOIN
- INNER JOIN vs LEFT JOIN
- Count rows per group (GROUP BY)
- Group with HAVING filter
- Multiple joins (3+ tables)
- Self-join (employee-manager)
- Nth-highest salary
- Top-3 per department
- Window functions: ROW_NUMBER
- Window functions: RANK vs DENSE_RANK
- (+ 10 more)

**Same structure as Task 2.1:** Create directories, write tests, implement, verify, commit.

---

### Task 2.3: Build SQL Advanced (21 questions)

**Questions:**

- Nested subqueries
- Correlated subqueries
- Common Table Expressions (WITH)
- UNION / UNION ALL
- Window functions: LAG/LEAD
- Recursive CTEs
- Date functions
- String functions
- Case statements
- JSON queries (basic)
- (+ 11 more)

---

## Phase 3: ML Compilers (Days 6-8, 23 questions)

### Task 3.1: ML Compilers Fundamentals (8 questions)

**Questions (easy to medium):**

1. Register Blocking: Intensity and Register Budget
2. A NumPy Interpreter for a Tiny Tensor IR
3. Map Loop Axes to CUDA Grid and Block Dimensions
4. Kernel Cache: Hash Compiled Kernels by Canonical Source
5. UOp Graph: Hash-Consing, Toposort and Node Counting
6. Algebraic Simplification with Canonical Forms
7. Interval Bounds for Symbolic Index Expressions
8. Views: Shape, Strides, Offset and Masks

**Structure:**
Each question includes a Python implementation + test suite. Example:

`data/app_data/05-deep-learning/07-ml-compilers/01-fundamentals/01-tensor-ir-interpreter/README.md`:

```markdown
---
name: mlc-numpy-interpreter-tensor-ir
topics: ['ML Compilers', 'Tensor Operations']
companies:
  names: ['OpenAI', 'Anthropic', 'Google Brain']
  roles: 'ML Systems / Compiler Engineer interviews'
---

# NumPy Interpreter for Tiny Tensor IR

## Problem

Implement a simple interpreter that takes a tiny tensor IR (intermediate representation)
and evaluates it using NumPy.

IR Operations:

- load(name) → load variable
- const(value) → constant
- reshape(expr, shape) → reshape
- dot(a, b) → matrix multiply
- add(a, b) → element-wise add

Example:
```

IR: dot(load('A'), load('B'))
Execute: np.dot(A, B)

```

## Your Task
Implement the `interpret` function that takes an IR expression and a dict of variables,
returning the computed NumPy result.
```

---

### Task 3.2: ML Compilers Intermediate (10 questions)

**Questions:**

- Render a Loopless Expression DAG to C and Run It
- Matmul and Conv2d from Movement Ops Only
- Kernel Splitting: Realize Reductions and Fuse the Rest
- Loop Tiling and Interchange on a Loop-Nest IR
- Unroll a Reduction into Chained Updates
- Online Softmax Attention as Coupled Accumulators
- Emulate a CUDA Kernel: Thread Grid, Guards and Coalescing Cost
- Render a Thread-Per-Element CUDA Kernel
- Adjoints of Movement Ops
- View Merging and the Contiguity Test

---

### Task 3.3: ML Compilers Advanced (5 questions)

**Questions:**

- Pattern Matching and Graph Rewrite to a Fixed Point
- Floor-Division and Modulo Folding for Index Math
- Rangeify: Push an Output Index Back Through Movement Ops
- Loop Nest Codegen for a Reduction: Render, Compile, Run
- Reverse-Mode Autodiff over a Tiny Graph IR

---

## Phase 4: DSA (Days 9-10, 20 high-impact questions)

### Task 4.1: Build DSA Fundamentals & Classic Structures (10 questions)

1. Implement a Trie for Prefix Matching
2. Implement a Hash Table from Scratch
3. Implement a Snapshot Array
4. Add Two Numbers as Linked Lists
5. Running Median of a Data Stream
6. Persistent LRU Cache
7. Queue from Two Stacks and a Min-Stack
8. Heap Drills: Top-K Frequent Elements
9. Binary Tree Drills: Diameter, Max Path Sum
10. Lowest Common Ancestor of a Binary Tree

Each follows TrenTorch structure with starter/solution/tests.

---

### Task 4.2: Build DSA Advanced (10 questions)

1. Token-Bucket Rate Limiter with Per-User Quotas
2. In-Memory Database with Insert and Filtered Select
3. Spreadsheet Formula Engine with Cycle Detection
4. Binary Tree Vertical Order Traversal
5. Dot Product of Two Sparse Vectors
6. Simple Order Book (Insert/Cancel/Match)
7. In-Memory Key-Value Store with TTL
8. Fixed-Size Block Memory Allocator
9. Thread-Safe Producer-Consumer Bounded Buffer
10. Banking Transaction System Core Logic

---

## Phase 5: Inference Gaps (Days 11, 8 questions)

### Task 5.1: Build Inference Performance Analysis

Add to `06-language-modelling-attention-llms/07-inference-optimization/`:

1. Roofline Model Analysis for GPU Operations
2. Compute Arithmetic Intensity and Classify Bottleneck
3. Classify LLM Prefill vs Decode as Compute-Bound or Memory-Bound
4. Estimate KV Cache Size from Model Config
5. Kernel Fusion Memory Savings Calculator
6. Cost per Million Tokens: Utilization & Blended Prices
7. The Price of Latency: Batch Size, Throughput and Cost per Token under an SLO
8. Goodput vs Throughput under a P99 SLA

All are numeric/analytical (no GPU needed), pure Python test-based.

---

## Phase 6: Distributed Training & Performance Optimization (Days 12-13, 18 questions)

### Task 6.1: Build Distributed Training Concepts (10 questions)

Add to `10-distributed-systems/02-distributed-training/`:

1. Data Parallelism: Replica Gradient Averaging
2. Model Parallelism: Split Layers Across Devices
3. Gradient Accumulation Mechanics
4. All-Reduce Communication Pattern Simulator
5. Allgather for Model Synchronization
6. Gradient Compression with Quantization
7. Mini Distributed Training in NumPy (DDP simulation)
8. Mixed-Precision Training: FP32/FP16 Scheduling
9. Loss Scaling for Gradient Underflow Prevention
10. ZeRO Optimizer: Memory Stage Analysis

---

### Task 6.2: Build Performance Optimization (8 questions)

Merge into `10-distributed-systems/03-performance-optimization/`:

1. Zero-Copy Batch Data Loading from Shared Memory
2. Environment Vectorization Auto-Configuration
3. Cython vs Python Performance Analysis
4. RL Training GPU Utilization Tracker
5. Memory Bandwidth Saturation Calculator
6. Cache-Aware Algorithm Design (data locality)
7. Vectorization Opportunity Detection
8. Algorithmic Complexity vs Constant Factors

---

## Testing & Validation

**Before each commit:**

```bash
# 1. Run curriculum build
node processes/curriculum-build/build.mjs

# 2. Run all local tests
pytest data/app_data/<track>/*/*/tests.py -v

# 3. Check formatting
npx prettier --check data/curriculum

# 4. Run build
npm run build
```

**After all phases:**

```bash
# Full validation
npm run lint && npm run check && npm run build
```

---

## Execution Strategy

**Option A: Subagent-Driven (Recommended)**

- One subagent per phase
- Each phase gets its own isolated context
- Parallel execution possible
- Better for 120+ questions

**Option B: Inline Sequential**

- Batch 3 tasks per iteration
- Lower context overhead
- Single thread, slower but simple

**Recommendation:** Go with **Subagent-Driven** to parallelize work and keep context fresh.

Start with Phase 1 (Infrastructure) inline to unblock Phase 2-6, then fan out subagents.
