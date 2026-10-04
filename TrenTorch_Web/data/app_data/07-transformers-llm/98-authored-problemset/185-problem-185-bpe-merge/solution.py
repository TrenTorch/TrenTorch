import numpy as np

def solve(seq, pair):
    """Merge non-overlapping occurrences of the requested adjacent token pair."""
        out=[]
        i=0
        while i<len(seq):
            if i+1<len(seq) and (seq[i],seq[i+1])==pair: out.append(seq[i]+seq[i+1]); i+=2
            else: out.append(seq[i]); i+=1
        return out
