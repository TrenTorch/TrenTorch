def test_max_min():
    cursor.execute(user_query)
    max_sal, min_sal = cursor.fetchone()
    assert max_sal == 90000 and min_sal == 30000, 'Correct max and min'
