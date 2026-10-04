import numpy as np

def solve(transactions, itemset):
    """Implement support counting according to the contract."""
    item = set(itemset)
    return sum((item.issubset(set(t)) for t in transactions)) / len(transactions)
