def test_not_condition():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 2, 'Should exclude Sales'
