"""Hidden tests: Partition Pruning with Range Predicates. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_count_is_correct(sql):
    sql.expect_rows([
        (248,),
    ], ordered=False)


def test_does_not_wrap_the_column_in_a_function(sql):
    text = sql.query.lower()
    assert "strftime" not in text and "substr" not in text and "like" not in text, (
        "Do not apply a function to event_date: compare the column itself with a start and end date."
    )


def test_plan_reads_only_a_range_of_the_index(sql):
    plan = " | ".join(sql.plan())
    assert "SEARCH" in plan and "idx_events_date" in plan, (
        "The plan should SEARCH idx_events_date (only March is read). Plan: " + plan
    )
