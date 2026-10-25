from itertools import product


def equations_possible(equations):
    letters = sorted({eq[0] for eq in equations} | {eq[3] for eq in equations})
    for values in product(range(len(letters)), repeat=len(letters)):
        value = dict(zip(letters, values))
        if all((value[eq[0]] == value[eq[3]]) == (eq[1] == "=") for eq in equations):
            return True
    return not letters or False
