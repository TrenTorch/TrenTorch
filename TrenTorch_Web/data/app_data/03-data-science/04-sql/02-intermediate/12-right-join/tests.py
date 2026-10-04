def test_right_join():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 2, 'Should return all users'
