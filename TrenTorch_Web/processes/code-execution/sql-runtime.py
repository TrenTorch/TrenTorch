"""SQL runtime shared by the in-browser worker (Pyodide) and the content tests.

The browser worker loads this file as text (`sql-runtime.py?raw`) and executes it
inside Pyodide; `data/app_data/03-data-science/04-sql/conftest.py` imports the very
same file so every question's tests.py runs under plain pytest against real SQLite.

Everything user-visible mimics the `sqlite3` command-line shell:
  * errors read `Parse error: near "FORM": syntax error` / `Runtime error: ...`
  * results render as an ASCII table with NULL shown literally
  * a script may hold several statements; the last one that returns rows is the result
"""

import json
import re
import sqlite3
import time
import traceback

MAX_ROWS_SHOWN = 100
MAX_ROWS_FETCHED = 50000
STATEMENT_TIME_LIMIT = 5.0

_PARSE_ERROR_HINTS = (
    "syntax error",
    "incomplete input",
    "no such table",
    "no such column",
    "no such function",
    "no such index",
    "no such view",
    "ambiguous column",
    "misuse of aggregate",
    "wrong number of arguments",
    "does not match",
    "already exists",
    "not authorized",
    "only a single result allowed",
    "row value misused",
    "is not a function",
    "second argument",
    "too many terms",
)


class SqlAssertionError(AssertionError):
    """An assertion that carries the expected/actual values for the results panel."""

    def __init__(self, message, expected=None, actual=None):
        super().__init__(message)
        self.expected = expected
        self.actual = actual


def has_sql(text):
    """True if `text` holds anything besides whitespace and comments."""
    stripped = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    stripped = re.sub(r"--[^\n]*", "", stripped)
    return bool(stripped.strip())


def split_statements(text):
    """Split a script into complete statements the way the sqlite3 shell does.

    A `;` ends a statement only when SQLite agrees the text so far is complete, so
    semicolons inside string literals, comments and CREATE TRIGGER bodies are safe,
    and several statements on one line are separated correctly.
    """
    statements = []
    start = 0
    for index, char in enumerate(text):
        if char == ";" and sqlite3.complete_statement(text[start : index + 1]):
            statements.append(text[start : index + 1].strip())
            start = index + 1
    tail = text[start:].strip()
    if tail:
        statements.append(tail)
    return [s for s in statements if has_sql(s)]


def format_error(error):
    """Render an exception the way the sqlite3 shell prints it."""
    message = str(error)
    lowered = message.lower()
    if isinstance(error, sqlite3.OperationalError):
        if "interrupted" in lowered:
            return (
                "Runtime error: interrupted\n"
                "The statement ran longer than %d seconds and was stopped. "
                "Check for a recursive CTE with no stop condition or a join with no ON clause."
                % STATEMENT_TIME_LIMIT
            )
        if any(hint in lowered for hint in _PARSE_ERROR_HINTS):
            return "Parse error: " + message
        return "Runtime error: " + message
    if isinstance(error, sqlite3.Error):
        return "Runtime error: " + message
    return "Error: " + message


def _cell(value):
    if value is None:
        return "NULL"
    if isinstance(value, bytes):
        return "x'" + value.hex() + "'"
    if isinstance(value, float):
        return repr(value)
    return str(value)


def render_table(columns, rows, elapsed):
    """Render a result set as an ASCII table followed by a row count line."""
    shown = rows[:MAX_ROWS_SHOWN]
    body = [[_cell(v) for v in row] for row in shown]
    widths = [len(str(name)) for name in columns]
    for row in body:
        for i, text in enumerate(row):
            widths[i] = max(widths[i], len(text))
    numeric = [
        bool(shown) and all(isinstance(row[i], (int, float)) for row in shown if row[i] is not None)
        and any(row[i] is not None for row in shown)
        for i in range(len(columns))
    ]

    def line(left, mid, right):
        return left + mid.join("-" * (w + 2) for w in widths) + right

    def fmt(cells, header=False):
        parts = []
        for i, text in enumerate(cells):
            parts.append(" " + (text.rjust(widths[i]) if numeric[i] and not header else text.ljust(widths[i])) + " ")
        return "|" + "|".join(parts) + "|"

    out = [line("+", "+", "+"), fmt([str(c) for c in columns], header=True), line("+", "+", "+")]
    out.extend(fmt(r) for r in body)
    out.append(line("+", "+", "+"))
    count = len(rows)
    summary = "%d row%s" % (count, "" if count == 1 else "s")
    if count == 0:
        summary = "Empty set"
    if count > MAX_ROWS_SHOWN:
        out.append("… %d more rows not shown" % (count - MAX_ROWS_SHOWN))
    out.append("%s (%.3f sec)" % (summary, elapsed))
    return "\n".join(out)


class StatementResult:
    def __init__(self, sql, columns=None, rows=None, rowcount=0, elapsed=0.0, error=None):
        self.sql = sql
        self.columns = columns
        self.rows = rows
        self.rowcount = rowcount
        self.elapsed = elapsed
        self.error = error


def connect():
    db = sqlite3.connect(":memory:")
    db.isolation_level = None  # autocommit; scripts manage their own transactions
    return db


def load_schema(db, schema):
    for statement in split_statements(schema or ""):
        db.execute(statement)


def run_script(db, script):
    """Run each statement; stop at the first error. Returns a list of StatementResult."""
    results = []
    for statement in split_statements(script):
        started = time.time()
        deadline = started + STATEMENT_TIME_LIMIT
        db.set_progress_handler(lambda: 1 if time.time() > deadline else 0, 10000)
        try:
            cursor = db.execute(statement)
            if cursor.description:
                columns = [d[0] for d in cursor.description]
                rows = cursor.fetchmany(MAX_ROWS_FETCHED + 1)
                if len(rows) > MAX_ROWS_FETCHED:
                    raise sqlite3.OperationalError(
                        "result set larger than %d rows" % MAX_ROWS_FETCHED
                    )
                results.append(
                    StatementResult(statement, columns, rows, len(rows), time.time() - started)
                )
            else:
                results.append(
                    StatementResult(statement, rowcount=max(cursor.rowcount, 0), elapsed=time.time() - started)
                )
        except Exception as error:  # noqa: BLE001 - every sqlite error is reported to the student
            results.append(StatementResult(statement, error=format_error(error)))
            break
        finally:
            db.set_progress_handler(None, 0)
    return results


def _first_line(statement):
    for line in statement.splitlines():
        if line.strip() and not line.strip().startswith("--"):
            return line.strip()[:90]
    return statement.strip()[:90]


def last_result_set(results):
    for result in reversed(results):
        if result.columns is not None:
            return result
    return None


def render_run(results):
    """(output_text, error_text) for the Console tab."""
    if not results:
        return "", "No SQL statement to run. Write a query in the editor first."
    multi = len(results) > 1
    blocks = []
    error = None
    for index, result in enumerate(results, start=1):
        header = "-- [%d] %s" % (index, _first_line(result.sql)) if multi else ""
        if result.error:
            error = result.error
            if multi:
                error += "\nWhile running statement %d: %s" % (index, _first_line(result.sql))
            else:
                error += "\nWhile running: " + _first_line(result.sql)
            break
        if result.columns is not None:
            body = render_table(result.columns, result.rows, result.elapsed)
        else:
            body = "Query OK, %d row%s affected (%.3f sec)" % (
                result.rowcount,
                "" if result.rowcount == 1 else "s",
                result.elapsed,
            )
        blocks.append((header + "\n" + body) if header else body)
    return "\n\n".join(blocks), error


class SqlContext:
    """The `sql` fixture handed to every test function."""

    def __init__(self, schema, query, extra_sql=""):
        self.schema = schema
        self.query = query
        self._extra_sql = extra_sql
        self.db = connect()
        load_schema(self.db, schema)
        if extra_sql:
            load_schema(self.db, extra_sql)
        self.results = run_script(self.db, query)
        self.error = next((r.error for r in self.results if r.error), None)
        self._set = last_result_set(self.results)

    # -- result access ------------------------------------------------------
    def _need_result(self):
        if self.error:
            raise SqlAssertionError("Your query failed to run.\n" + self.error)
        if self._set is None:
            raise SqlAssertionError(
                "Your script did not return a result set. End it with a SELECT statement."
            )
        return self._set

    @property
    def columns(self):
        return [c.lower() for c in self._need_result().columns]

    @property
    def rows(self):
        return [tuple(r) for r in self._need_result().rows]

    @property
    def records(self):
        cols = self._need_result().columns
        return [dict(zip(cols, r)) for r in self._need_result().rows]

    @property
    def final_select(self):
        """Text of the last statement that returned rows (for EXPLAIN QUERY PLAN checks)."""
        return self._need_result().sql.rstrip().rstrip(";")

    @property
    def statements(self):
        return [r.sql for r in self.results]

    # -- helpers for tests --------------------------------------------------
    def run(self, sql_text):
        """Run extra SQL on the student's database (after their script ran)."""
        cursor = self.db.execute(sql_text)
        return [tuple(r) for r in cursor.fetchall()] if cursor.description else []

    def plan(self, select_sql=None):
        """The `detail` column of EXPLAIN QUERY PLAN for a SELECT (default: the student's)."""
        text = select_sql if select_sql is not None else self.final_select
        return [row[-1] for row in self.db.execute("EXPLAIN QUERY PLAN " + text).fetchall()]

    def table_exists(self, name):
        found = self.db.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (name,)
        ).fetchone()
        return found is not None

    def index_columns(self, table):
        """{index_name: [columns]} for every index on `table`."""
        found = {}
        for row in self.db.execute("PRAGMA index_list(%s)" % table).fetchall():
            name = row[1]
            found[name] = [c[2] for c in self.db.execute("PRAGMA index_info(%s)" % name).fetchall()]
        return found

    def with_data(self, extra_sql):
        """Re-run the student's script against the schema plus `extra_sql` (hidden data)."""
        return SqlContext(self.schema, self.query, extra_sql)

    def expect_rows(self, expected, ordered=True):
        actual = self.rows
        want = [tuple(r) for r in expected]
        if not ordered:
            key = lambda r: tuple((v is None, str(v)) for v in r)  # noqa: E731
            got_cmp, want_cmp = sorted(actual, key=key), sorted(want, key=key)
        else:
            got_cmp, want_cmp = actual, want
        if len(actual) != len(want):
            raise SqlAssertionError(
                "Expected %d row%s but your query returned %d."
                % (len(want), "" if len(want) == 1 else "s", len(actual)),
                expected=repr(want),
                actual=repr(actual),
            )
        if got_cmp != want_cmp:
            raise SqlAssertionError(
                "The rows do not match what the question asks for"
                + ("" if ordered else " (row order does not matter here)")
                + ".",
                expected=repr(want),
                actual=repr(actual),
            )

    def expect_columns(self, expected):
        actual = self.columns
        want = [c.lower() for c in expected]
        if actual != want:
            raise SqlAssertionError(
                "Expected the columns %s, in this order." % ", ".join(want),
                expected=repr(want),
                actual=repr(actual),
            )

    def expect_column_count(self, count):
        actual = self.columns
        if len(actual) != count:
            raise SqlAssertionError(
                "Expected %d column%s but your query returned %d: %s."
                % (count, "" if count == 1 else "s", len(actual), ", ".join(actual)),
                expected=str(count),
                actual=str(len(actual)),
            )

    def close(self):
        try:
            self.db.close()
        except Exception:  # noqa: BLE001
            pass


def _failure_reason(error, name, test_code_lines):
    detail = str(error).strip()
    if isinstance(error, AssertionError):
        reason = detail if detail else "Assertion failed."
    else:
        reason = type(error).__name__ + (": " + detail if detail else "")
    frames = traceback.extract_tb(error.__traceback__)
    frame = next((f for f in reversed(frames) if f.name == name and f.filename == "<tests>"), None)
    if frame and not isinstance(error, SqlAssertionError) and test_code_lines:
        if 0 < frame.lineno <= len(test_code_lines):
            reason += "\nLine %d: %s" % (frame.lineno, test_code_lines[frame.lineno - 1].strip())
    return reason


def collect_and_run(tests_code, make_context):
    """Run every module-level test_* function in `tests_code`. Returns result dicts."""
    namespace = {"__name__": "sql_tests"}
    exec(compile(tests_code, "<tests>", "exec"), namespace)
    names = sorted(n for n, f in namespace.items() if n.startswith("test_") and callable(f))
    lines = tests_code.splitlines()
    ctx = make_context()
    results = []
    try:
        if ctx.error or not ctx.results:
            # A script that does not run cannot pass anything; say why once per test.
            reason = (
                "Your query failed to run.\n" + ctx.error
                if ctx.error
                else "There is no SQL statement in the editor yet. Write your query and submit again."
            )
            return [{"name": n, "passed": False, "error": reason, "durationMs": 0} for n in names]
        for name in names:
            started = time.time()
            try:
                parameters = list(__import__("inspect").signature(namespace[name]).parameters)
                if parameters not in ([], ["sql"]):
                    raise TypeError("test fixture %r is not available" % parameters[0])
                namespace[name](ctx) if parameters else namespace[name]()
                results.append({"name": name, "passed": True, "error": None})
            except Exception as error:  # noqa: BLE001
                entry = {"name": name, "passed": False, "error": _failure_reason(error, name, lines)}
                if isinstance(error, SqlAssertionError):
                    entry["expected"] = error.expected
                    entry["actual"] = error.actual
                results.append(entry)
            results[-1]["durationMs"] = int((time.time() - started) * 1000)
    finally:
        ctx.close()
    return results


# -- entry points called by the worker ----------------------------------------
def entry_run(query, schema):
    started = time.time()
    db = connect()
    try:
        try:
            load_schema(db, schema)
        except Exception as error:  # noqa: BLE001
            return json.dumps(
                {
                    "output": "",
                    "error": "This question's tables failed to load: " + str(error),
                    "ms": 0,
                }
            )
        results = run_script(db, query)
        output, error = render_run(results)
        return json.dumps({"output": output, "error": error, "ms": int((time.time() - started) * 1000)})
    finally:
        db.close()


def entry_test(query, schema, tests_code):
    started = time.time()
    try:
        results = collect_and_run(tests_code, lambda: SqlContext(schema, query))
        return json.dumps({"results": results, "error": None, "ms": int((time.time() - started) * 1000)})
    except Exception:  # noqa: BLE001 - a broken tests file is a content bug, not the student's
        return json.dumps(
            {"results": [], "error": "Test harness failed:\n" + traceback.format_exc(), "ms": 0}
        )
