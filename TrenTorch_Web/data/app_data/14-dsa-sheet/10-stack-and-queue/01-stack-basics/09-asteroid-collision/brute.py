def asteroid_collision(asteroids):
    a = list(asteroids)
    while True:
        for i in range(len(a) - 1):
            if a[i] > 0 and a[i + 1] < 0:
                if a[i] > -a[i + 1]:
                    del a[i + 1]
                elif a[i] < -a[i + 1]:
                    del a[i]
                else:
                    del a[i : i + 2]
                break
        else:
            return a
