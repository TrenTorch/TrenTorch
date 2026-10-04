# SQL Tests for SELECT All Rows
# The executor runs the user query and validates results

def test_returns_all_rows():
    """Test that the query returns all 3 users"""
    # cursor and db are provided by executor
    # User query result should have 3 rows
    assert len(cursor.fetchall()) == 3, "Query should return all 3 users"

def test_returns_all_columns():
    """Test that the query returns all columns"""
    # Should return id, name, email, age for each row
    cursor.execute(user_query)
    row = cursor.fetchone()
    assert len(row) == 4, "Should return all 4 columns"
