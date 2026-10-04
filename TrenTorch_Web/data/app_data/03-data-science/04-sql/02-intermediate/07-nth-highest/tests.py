def test_nth_highest():
    cursor.execute(user_query)
    salary = cursor.fetchone()[0]
    assert salary == 80000, 'Third highest should be 80000'
