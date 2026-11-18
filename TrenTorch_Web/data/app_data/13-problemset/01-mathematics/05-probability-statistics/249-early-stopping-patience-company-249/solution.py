def solve(losses,patience):
    best=float('inf'); bad=0
    for i,x in enumerate(losses):
        if x<best: best=x; bad=0
        else:
            bad+=1
            if bad>=patience: return i
    return -1
