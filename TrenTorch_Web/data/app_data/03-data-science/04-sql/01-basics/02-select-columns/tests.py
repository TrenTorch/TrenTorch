def test_returns_two_columns():
    cursor.execute(user_query)
    row = cursor.fetchone()
    assert len(row) == 2, 'Should return exactly 2 columns'

def test_returns_correct_columns():
    cursor.execute(user_query)
    assert cursor.description[0][0] == 'id', 'First column should be id'
    assert cursor.description[1][0] == 'name', 'Second column should be name'

def test_returns_three_rows():
    cursor.execute(user_query)
    assert len(cursor.fetchall()) == 3, 'Should return 3 rows'
