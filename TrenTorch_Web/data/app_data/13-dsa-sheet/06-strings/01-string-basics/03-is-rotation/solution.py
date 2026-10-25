def is_rotation(s, goal):
    return len(s) == len(goal) and goal in s + s
