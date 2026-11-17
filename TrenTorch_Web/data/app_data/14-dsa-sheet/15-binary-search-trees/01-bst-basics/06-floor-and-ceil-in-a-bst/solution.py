class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def floor_and_ceil_bst(root, x):
    floor = ceil = -1
    node = root
    while node:
        if node.val == x:
            return [x, x]
        if node.val < x:
            floor = node.val
            node = node.right
        else:
            ceil = node.val
            node = node.left
    return [floor, ceil]
