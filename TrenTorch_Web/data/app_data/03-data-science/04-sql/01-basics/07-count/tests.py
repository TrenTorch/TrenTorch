def test_counts_all_rows():
    cursor.execute(user_query)
    count = cursor.fetchone()[0]
    assert count == 3, 'Should count 3 users'
