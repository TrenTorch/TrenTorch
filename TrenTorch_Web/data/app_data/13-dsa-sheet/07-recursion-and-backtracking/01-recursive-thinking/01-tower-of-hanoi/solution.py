def tower_of_hanoi(n):
    moves = []

    def move(k, source, target, spare):
        if k == 0:
            return
        move(k - 1, source, spare, target)
        moves.append([source, target])
        move(k - 1, spare, target, source)

    move(n, 1, 3, 2)
    return moves
