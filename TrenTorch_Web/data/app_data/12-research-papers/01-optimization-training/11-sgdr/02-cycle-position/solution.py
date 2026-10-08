def sgdr_position(t, T0, Tmult):
    T_i = T0
    while t >= T_i:
        t -= T_i
        T_i *= Tmult
    return t, T_i
