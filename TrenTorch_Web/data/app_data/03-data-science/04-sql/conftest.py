"""Makes every SQL question's tests.py runnable under plain pytest.

In the browser the SQL worker hands each test a `sql` fixture; this conftest builds
the identical object from the same runtime file (processes/code-execution/sql-runtime.py),
using the question's starter.py for the schema and solution.py as the "student" query,
so `pytest data/app_data` proves that every reference solution passes its own tests on
real SQLite.
"""

import importlib.util
from pathlib import Path

import pytest

_RUNTIME = Path(__file__).resolve().parents[4] / "processes" / "code-execution" / "sql-runtime.py"
_spec = importlib.util.spec_from_file_location("sql_runtime", _RUNTIME)
sql_runtime = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sql_runtime)

SCHEMA_MARKER = "-- @schema"
QUERY_MARKER = "-- @query"


def split_starter(text):
    """Mirror of splitSqlStarter() in processes/ide-content/sql-question.ts."""
    schema_at, query_at = text.find(SCHEMA_MARKER), text.find(QUERY_MARKER)
    assert 0 <= schema_at < query_at, "starter.py needs '-- @schema' followed by '-- @query'"
    return text[schema_at + len(SCHEMA_MARKER) : query_at].strip(), text[query_at + len(QUERY_MARKER) :].strip()


@pytest.fixture
def sql(request):
    folder = Path(request.path).parent
    schema, _ = split_starter((folder / "starter.py").read_text())
    context = sql_runtime.SqlContext(schema, (folder / "solution.py").read_text())
    yield context
    context.close()
