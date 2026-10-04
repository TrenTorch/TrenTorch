import numpy as np

def solve(splits):
        imp={}
        for feature,reduction in splits: imp[feature]=imp.get(feature,0.0)+reduction
        total=sum(imp.values())
        return {k:v/total for k,v in imp.items()} if total else imp
