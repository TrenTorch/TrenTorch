def count_reverse_pairs(nums):
    def sort(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, x = sort(a[:mid])
        right, y = sort(a[mid:])
        count = x + y
        j = 0
        for v in left:
            while j < len(right) and v > 2 * right[j]:
                j += 1
            count += j
        return sorted(left + right), count

    return sort(list(nums))[1]
