def test_cross_join():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 4, 'Should return 2x2 = 4 combinations'
