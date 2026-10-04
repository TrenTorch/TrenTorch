import numpy as np

def solve(transactions, itemset):
    """Support is the fraction of transactions that contain every item in the queried itemset."""
    item=set(itemset); return sum(item.issubset(set(t)) for t in transactions)/len(transactions) if transactions else 0.0
