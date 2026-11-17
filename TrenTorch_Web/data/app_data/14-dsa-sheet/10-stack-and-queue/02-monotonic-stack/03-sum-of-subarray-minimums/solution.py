def sum_subarray_mins(arr):
    n = len(arr)
    left = [0] * n
    right = [0] * n
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)
    return sum(arr[i] * (i - left[i]) * (right[i] - i) for i in range(n)) % (10**9 + 7)
