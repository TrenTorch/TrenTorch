def test_finds_null_manager():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 1, 'Should find 1 manager'
