def test_returns_matching_depts():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 2, 'Should return 2 rows'
