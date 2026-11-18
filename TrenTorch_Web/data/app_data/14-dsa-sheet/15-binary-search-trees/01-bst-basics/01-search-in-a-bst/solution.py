class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def search_bst(root, val):
    node = root
    while node and node.val != val:
        node = node.left if val < node.val else node.right
    return node
