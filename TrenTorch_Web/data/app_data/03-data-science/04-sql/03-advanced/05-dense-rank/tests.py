def test_dense_rank():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 3, 'Should return 3 employees'
