def first_finish_index(actions):
    for i, (name, _arg) in enumerate(actions):
        if name == "Finish":
            return i
    return None
