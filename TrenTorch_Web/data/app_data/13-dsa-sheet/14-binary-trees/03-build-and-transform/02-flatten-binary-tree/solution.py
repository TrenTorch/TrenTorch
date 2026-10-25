class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def flatten_tree(root):
    node = root
    while node:
        if node.left:
            tail = node.left
            while tail.right:
                tail = tail.right
            tail.right = node.right
            node.right = node.left
            node.left = None
        node = node.right
    return root
