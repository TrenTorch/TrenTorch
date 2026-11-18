def spiral_order(matrix):
    if not matrix or not matrix[0]:
        return []
    out = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        out.extend(matrix[top][left : right + 1])
        for i in range(top + 1, bottom + 1):
            out.append(matrix[i][right])
        if top < bottom:
            out.extend(reversed(matrix[bottom][left:right]))
        if left < right:
            for i in range(bottom - 1, top, -1):
                out.append(matrix[i][left])
        top += 1
        bottom -= 1
        left += 1
        right -= 1
    return out
