class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def bst_from_preorder(preorder):
    index = 0

    def build(bound):
        nonlocal index
        if index == len(preorder) or preorder[index] > bound:
            return None
        node = TreeNode(preorder[index])
        index += 1
        node.left = build(node.val)
        node.right = build(bound)
        return node

    return build(float("inf"))
