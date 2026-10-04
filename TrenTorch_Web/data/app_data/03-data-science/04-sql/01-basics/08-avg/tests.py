def test_calculates_average():
    cursor.execute(user_query)
    avg = cursor.fetchone()[0]
    assert abs(avg - 30.0) < 0.01, 'Average age should be 30'
