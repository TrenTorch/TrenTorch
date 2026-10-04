def test_date_diff():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 2, 'Should return 2 employees with days employed'
