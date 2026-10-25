class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def merge_bsts(root1: TreeNode | None, root2: TreeNode | None) -> list[int]:
    """Return all the values of both trees in increasing order."""
    # This is correct but does not use the BST order: it collects everything and sorts.
    values = []
    for root in (root1, root2):
        stack = [root] if root else []
        while stack:
            node = stack.pop()
            values.append(node.val)
            stack.extend(c for c in (node.left, node.right) if c)
    return sorted(values)
