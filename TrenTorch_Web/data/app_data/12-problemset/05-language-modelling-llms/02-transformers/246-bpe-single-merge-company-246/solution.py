def solve(tokens,a,b,merged):
    out=[]; i=0
    while i<len(tokens):
        if i+1<len(tokens) and tokens[i]==a and tokens[i+1]==b: out.append(merged); i+=2
        else: out.append(tokens[i]); i+=1
    return out
