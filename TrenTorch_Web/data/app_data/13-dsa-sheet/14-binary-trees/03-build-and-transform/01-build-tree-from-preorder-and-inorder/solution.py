class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(preorder, inorder):
    pos = {v: i for i, v in enumerate(inorder)}
    values = iter(preorder)

    def build(lo, hi):
        if lo >= hi:
            return None
        root = TreeNode(next(values))
        mid = pos[root.val]
        root.left = build(lo, mid)
        root.right = build(mid + 1, hi)
        return root

    return build(0, len(inorder))
