def find_target(root, k):
    def ascending(node):
        stack = []
        while node or stack:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.val
            node = node.right

    def descending(node):
        stack = []
        while node or stack:
            while node:
                stack.append(node)
                node = node.right
            node = stack.pop()
            yield node.val
            node = node.left

    up, down = ascending(root), descending(root)
    lo, hi = next(up, None), next(down, None)
    while lo is not None and hi is not None and lo < hi:
        total = lo + hi
        if total == k:
            return True
        if total < k:
            lo = next(up, None)
        else:
            hi = next(down, None)
    return False
