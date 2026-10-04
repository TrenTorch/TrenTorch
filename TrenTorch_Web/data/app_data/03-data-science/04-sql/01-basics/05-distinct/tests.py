def test_returns_distinct_ages():
    cursor.execute(user_query)
    ages = [row[0] for row in cursor.fetchall()]
    assert len(ages) == 3, 'Should return 3 distinct ages'
