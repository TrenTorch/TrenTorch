import numpy as np

def solve(beams,next_logp,width):
    cand=[]
    for seq,score in beams:
        for tok,lp in enumerate(next_logp): cand.append((seq+[tok],score+float(lp)))
    cand.sort(key=lambda x:(-x[1],x[0])); return cand[:width]
