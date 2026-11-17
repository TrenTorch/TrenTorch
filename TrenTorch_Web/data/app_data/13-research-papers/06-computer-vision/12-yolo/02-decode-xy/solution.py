import math


def decode_xy(sx, sy, col, row, S, img):
    cell = img / S
    x = (col + 1 / (1 + math.exp(-sx))) * cell
    y = (row + 1 / (1 + math.exp(-sy))) * cell
    return (x, y)
