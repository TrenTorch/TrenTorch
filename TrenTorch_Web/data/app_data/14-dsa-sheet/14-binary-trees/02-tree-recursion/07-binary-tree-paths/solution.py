class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def root_to_leaf_paths(root):
    out = []

    def go(node, path):
        if node is None:
            return
        path.append(str(node.val))
        if node.left is None and node.right is None:
            out.append("->".join(path))
        else:
            go(node.left, path)
            go(node.right, path)
        path.pop()

    go(root, [])
    return out
