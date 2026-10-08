def sgdr_position(t, T0, Tmult):
    """
    t: global step; T0: first cycle length; Tmult: cycle length multiplier per restart

    Returns:
        (t_cur, T_i): steps since the last restart and the length of the current cycle.
    """
    # TODO: Subtract whole cycles from t, growing the cycle length by Tmult each time (see Theory).
    pass
