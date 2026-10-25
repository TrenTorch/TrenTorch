class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def recover_tree(root):
    first = second = prev = None
    stack = []
    node = root
    while node or stack:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev is not None and prev.val > node.val:
            if first is None:
                first = prev
            second = node
        prev = node
        node = node.right
    first.val, second.val = second.val, first.val
    return root
