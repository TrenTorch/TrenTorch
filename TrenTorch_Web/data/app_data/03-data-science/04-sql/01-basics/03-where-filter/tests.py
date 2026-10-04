def test_filters_by_age():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    assert len(rows) == 2, 'Should return 2 rows (Bob and Charlie)'

def test_excludes_alice():
    cursor.execute(user_query)
    names = [row[1] for row in cursor.fetchall()]
    assert 'Alice' not in names, 'Alice (age 25) should be excluded'
