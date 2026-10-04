def test_pattern_matching():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 2, 'Should match Alice and Charlie'
