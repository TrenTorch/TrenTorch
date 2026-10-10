import numpy as np

def solve(transactions,itemset):
        item=set(itemset); return sum(item.issubset(set(t)) for t in transactions)/len(transactions)
