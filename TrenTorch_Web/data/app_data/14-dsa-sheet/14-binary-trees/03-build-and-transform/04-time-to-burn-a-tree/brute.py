class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def to_list(root):
    """Level order with None for missing children, trailing Nones removed."""
    if root is None:
        return []
    out = []
    queue = [root]
    i = 0
    while i < len(queue):
        node = queue[i]
        i += 1
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def from_list(items):
    if not items or items[0] is None:
        return None
    root = TreeNode(items[0])
    queue = [root]
    i = 1
    for node in queue:
        if i < len(items) and items[i] is not None:
            node.left = TreeNode(items[i])
            queue.append(node.left)
        i += 1
        if i < len(items) and items[i] is not None:
            node.right = TreeNode(items[i])
            queue.append(node.right)
        i += 1
    return root


def burn_time(root, start):
    edges = {root.val: []}

    def walk(node):
        for child in (node.left, node.right):
            if child:
                edges.setdefault(node.val, []).append(child.val)
                edges.setdefault(child.val, []).append(node.val)
                walk(child)

    walk(root)
    dist = {start: 0}
    todo = [start]
    for v in todo:
        for w in edges[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                todo.append(w)
    return max(dist.values())
