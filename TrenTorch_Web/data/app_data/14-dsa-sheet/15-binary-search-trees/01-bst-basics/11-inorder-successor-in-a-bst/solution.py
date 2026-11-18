class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def inorder_successor(root, p):
    answer = None
    node = root
    while node:
        if node.val > p:
            answer = node
            node = node.left
        else:
            node = node.right
    return answer
