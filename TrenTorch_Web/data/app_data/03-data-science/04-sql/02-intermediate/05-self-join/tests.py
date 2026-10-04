def test_self_join():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 3, 'Should return all employees'
