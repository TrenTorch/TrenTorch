def test_distinct_count():
    cursor.execute(user_query)
    count = cursor.fetchone()[0]
    assert count == 3, 'Should have 3 distinct departments'
