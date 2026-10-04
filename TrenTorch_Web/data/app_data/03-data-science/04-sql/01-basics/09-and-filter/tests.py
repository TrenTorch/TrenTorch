def test_filters_both_conditions():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 1, 'Should return 1 row (Bob)'
