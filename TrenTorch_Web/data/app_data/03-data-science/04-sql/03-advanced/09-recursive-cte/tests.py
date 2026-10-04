def test_recursive_cte():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 5, 'Should generate 5 numbers'
