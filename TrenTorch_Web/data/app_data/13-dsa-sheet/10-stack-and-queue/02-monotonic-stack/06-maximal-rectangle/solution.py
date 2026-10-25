def maximal_rectangle(matrix):
    if not matrix:
        return 0
    cols = len(matrix[0])
    heights = [0] * cols
    best = 0

    def largest_in_histogram(hs):
        result = 0
        stack = []
        for i, h in enumerate(hs + [0]):
            while stack and hs[stack[-1]] >= h:
                height = hs[stack.pop()]
                left = stack[-1] if stack else -1
                result = max(result, height * (i - left - 1))
            stack.append(i)
        return result

    for row in matrix:
        for j in range(cols):
            heights[j] = heights[j] + 1 if row[j] else 0
        best = max(best, largest_in_histogram(heights))
    return best
