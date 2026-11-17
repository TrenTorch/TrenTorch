def refine_loop(generate, feedback, refine, steps):
    y = generate()
    for _ in range(steps):
        fb = feedback(y)
        if fb == "OK":
            break
        y = refine(y, fb)
    return y
