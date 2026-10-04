def test_union():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 4, 'Should return 4 unique names'
