def f(x):
    eps = 1e-8
    bs = range(-1,-10,-1)
    for b in bs:
        c = 10**b
        #if abs(x%c - x) >= eps:
        if abs(x%c) < eps:
            return b

