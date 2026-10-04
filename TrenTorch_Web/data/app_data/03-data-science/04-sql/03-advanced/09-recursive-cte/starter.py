def solve():
    """
    TODO: Implement your solution here.

    Problem: Recursive CTEs
    Description: WITH RECURSIVE nums(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM nums WHERE n < 10) SELECT * FROM nums
    """
    pass
