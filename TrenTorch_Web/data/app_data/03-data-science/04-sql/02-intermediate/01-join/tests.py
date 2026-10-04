def test_inner_join():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 2, 'Should return 2 matched rows'
