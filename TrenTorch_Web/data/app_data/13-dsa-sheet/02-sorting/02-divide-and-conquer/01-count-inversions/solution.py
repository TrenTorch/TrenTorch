def count_inversions(nums):
    def sort(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, x = sort(a[:mid])
        right, y = sort(a[mid:])
        merged = []
        i = j = cross = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                cross += len(left) - i
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, x + y + cross

    return sort(list(nums))[1]
