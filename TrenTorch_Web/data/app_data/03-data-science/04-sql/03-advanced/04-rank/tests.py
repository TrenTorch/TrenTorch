def test_rank():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 4, 'Should return 4 employees with ranks'
