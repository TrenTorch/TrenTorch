def test_sorts_by_age_descending():
    cursor.execute(user_query)
    rows = cursor.fetchall()
    ages = [row[2] for row in rows]
    assert ages == [35, 30, 25], 'Should be sorted by age descending'
