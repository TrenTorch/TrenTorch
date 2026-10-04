def test_having_clause():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 1, 'Should return only Sales dept'
