def test_returns_three_rows():
    cursor.execute(user_query)
    assert len(cursor.fetchall()) == 3, 'Should return exactly 3 rows'
