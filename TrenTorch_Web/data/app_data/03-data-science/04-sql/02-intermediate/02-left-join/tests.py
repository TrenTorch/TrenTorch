def test_left_join():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 3, 'Should return all users (including Charlie with NULL)'
