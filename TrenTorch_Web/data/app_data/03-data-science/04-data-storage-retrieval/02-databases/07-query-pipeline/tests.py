"""
pytest tests.py
"""

import inspect

from _load import load_solution

_module = load_solution(__file__)
scan = _module.scan
filter_rows = _module.filter_rows
project = _module.project
order_by = _module.order_by
limit = _module.limit
run_query = _module.run_query

USERS = [
    {"name": "Dev", "age": 35, "city": "pune"},
    {"name": "Asha", "age": 28, "city": "delhi"},
    {"name": "Chen", "age": 41, "city": "pune"},
    {"name": "Bela", "age": 35, "city": "goa"},
]


def _counting(rows):
    pulled = []

    def generator():
        for row in rows:
            pulled.append(row)
            yield row

    return generator(), pulled


# ---- 1-5: the operators are lazy generators ----


def test_1_the_streaming_operators_are_generator_functions():
    for fn in (scan, filter_rows, project, limit, order_by):
        assert inspect.isgeneratorfunction(fn)


def test_2_scan_yields_the_rows_in_order():
    assert list(scan(USERS)) == USERS


def test_3_filter_keeps_only_matching_rows_in_order():
    assert [r["name"] for r in filter_rows(scan(USERS), lambda r: r["age"] > 30)] == ["Dev", "Chen", "Bela"]


def test_4_project_builds_new_narrow_rows_in_the_listed_order():
    out = list(project(scan(USERS), ["city", "name"]))
    assert out[0] == {"city": "pune", "name": "Dev"}
    assert list(out[0].keys()) == ["city", "name"]
    assert "age" in USERS[0]


def test_5_nothing_is_pulled_until_the_result_is_requested():
    source, pulled = _counting(USERS)
    stream = filter_rows(project(source, ["name", "age"]), lambda r: r["age"] > 0)
    assert pulled == []
    next(stream)
    assert len(pulled) == 1


# ---- 6-9: limit ----


def test_6_limit_yields_at_most_n_rows():
    assert [r["name"] for r in limit(scan(USERS), 2)] == ["Dev", "Asha"]


def test_7_limit_stops_pulling_after_n_rows():
    source, pulled = _counting(USERS)
    assert len(list(limit(source, 2))) == 2
    assert len(pulled) == 2


def test_8_limit_larger_than_the_input_and_non_positive_limits():
    assert len(list(limit(scan(USERS), 100))) == 4
    source, pulled = _counting(USERS)
    assert list(limit(source, 0)) == [] and pulled == []
    assert list(limit(scan(USERS), -3)) == []


def test_9_limit_after_filter_only_reads_as_much_as_it_needs():
    big = [{"v": i} for i in range(10_000)]
    source, pulled = _counting(big)
    out = list(limit(filter_rows(source, lambda r: r["v"] % 2 == 0), 5))
    assert [r["v"] for r in out] == [0, 2, 4, 6, 8] and len(pulled) == 9


# ---- 10-14: order by ----


def test_10_ascending_and_descending_order():
    ascending = [r["name"] for r in order_by(scan(USERS), "name")]
    descending = [r["name"] for r in order_by(scan(USERS), "name", descending=True)]
    assert ascending == ["Asha", "Bela", "Chen", "Dev"]
    assert descending == ["Dev", "Chen", "Bela", "Asha"]


def test_11_sort_is_stable_in_both_directions():
    asc = [r["name"] for r in order_by(scan(USERS), "age")]
    desc = [r["name"] for r in order_by(scan(USERS), "age", descending=True)]
    assert asc == ["Asha", "Dev", "Bela", "Chen"]
    assert desc == ["Chen", "Dev", "Bela", "Asha"]


def test_12_nones_sort_last_in_both_directions():
    rows = [{"v": 2}, {"v": None}, {"v": 1}]
    assert [r["v"] for r in order_by(rows, "v")] == [1, 2, None]
    assert [r["v"] for r in order_by(rows, "v", descending=True)] == [2, 1, None]


def test_13_order_by_is_blocking_and_reads_everything_before_yielding():
    source, pulled = _counting(USERS)
    stream = order_by(source, "age")
    next(stream)
    assert len(pulled) == 4


def test_14_order_by_does_not_modify_the_input():
    rows = [dict(r) for r in USERS]
    list(order_by(rows, "age"))
    assert rows == USERS


# ---- 15-20: whole queries ----


def test_15_select_where_order_limit():
    # SELECT name FROM users WHERE age > 30 ORDER BY age DESC LIMIT 2
    out = run_query(USERS, where=lambda r: r["age"] > 30, columns=["name"], order_column="age", descending=True, row_limit=2)
    assert out == [{"name": "Chen"}, {"name": "Dev"}]


def test_16_defaults_return_the_whole_table_as_a_list():
    out = run_query(USERS)
    assert out == USERS and isinstance(out, list)


def test_17_sort_column_need_not_be_projected():
    out = run_query(USERS, columns=["name"], order_column="age")
    assert [r["name"] for r in out] == ["Asha", "Dev", "Bela", "Chen"]
    assert all(list(r.keys()) == ["name"] for r in out)


def test_18_filter_runs_before_limit():
    out = run_query(USERS, where=lambda r: r["city"] == "pune", row_limit=1)
    assert [r["name"] for r in out] == ["Dev"]


def test_19_sort_runs_before_limit():
    out = run_query(USERS, order_column="name", row_limit=2, columns=["name"])
    assert [r["name"] for r in out] == ["Asha", "Bela"]


def test_20_the_table_is_not_modified_and_a_limit_without_a_sort_reads_few_rows():
    table = [dict(r) for r in USERS]
    run_query(table, where=lambda r: True, columns=["name"], order_column="name", row_limit=1)
    assert table == USERS
    big = [{"v": i} for i in range(5000)]
    source, pulled = _counting(big)
    assert len(list(limit(filter_rows(scan(source), lambda r: True), 3))) == 3
    assert len(pulled) == 3
