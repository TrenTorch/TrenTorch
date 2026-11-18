> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Binary trees)

This page teaches binary trees from the very first picture to some of the classic interview tricks. It assumes only that you can write a loop and a simple function. You will learn what a tree is, the different ways to walk through all of its nodes, how to solve problems by trusting recursion, how to rebuild a tree from its traversals, and how to treat a tree like a map of roads.

The page is a staircase. **Chapter 1 is deliberately gentle**: just the shape of a tree and one small recursive idea, with no heavy math. Every chapter after it adds one new family of problems, and each one only uses what came before. By the last chapter you will be ready for the hardest questions in this step. Every code example is shown in Python and in C++, so use whichever language you like.

# Chapter 1. What a tree is

## 1.1 Pictures of a tree

A **tree** is a way of storing things where every item points down to at most a few other items. The picture is an upside-down tree: one item sits at the top, and the rest hang below it.

```
        8
       / \
      3   10
     / \    \
    1   6    14
```

Each circle (here, each number) is called a **node**. The top node, `8`, is the **root**. A line from a node down to the node below it is an **edge**. The node above is the **parent**, the node below is its **child**. Here `3` is the parent of `1` and `6`, and `1` and `6` are the **children** of `3`. A node with no children, like `1`, `6` or `14`, is a **leaf**.

In a **binary** tree, every node has at most two children, and we call them the **left child** and the **right child**. A node may have just one of them (like `10`, which has only a right child), or none at all.

Here is the most important idea of the whole page. Pick any node, for example `3`. The node together with everything hanging below it is again a tree, a smaller one. We call it the **subtree** of that node. So a tree is a root plus a left subtree plus a right subtree, and each of those is again a tree. This "tree made of smaller trees" is the reason recursion fits trees so perfectly.

Two more words you will meet often. The **depth** of a node is how many edges you walk from the root down to it (the root has depth 0, so `1` has depth 2). The **height** of a tree is the largest depth of any node, so the tree above has height 2. In some problems people count nodes instead of edges, and then the height is 3. Always read the statement to see which one is meant.

## 1.2 Writing a node in code

To store a tree in a program we make one small object per node. Each node remembers its own value and two links, one to the left child and one to the right child. A link that leads nowhere holds "nothing" (`None` in Python, `nullptr` in C++). A whole tree is simply the node at its root, because from the root we can reach every other node by following links.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def make_small_tree():
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    return root


small = make_small_tree()
assert small.val == 1
assert small.left.val == 2 and small.right.val == 3
assert small.left.left is None
```

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {}
};

TreeNode* make_small_tree() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    return root;
}
```

Building a tree link by link gets tiring fast. In the sheet, and in most interview problems, a tree is written as a **level-order list**: the values row by row from left to right, with `None` standing for a missing child. So `[3, 9, 20, None, None, 15, 7]` means a root `3` with children `9` and `20`, where `9` has no children and `20` has children `15` and `7`. The helper below turns such a list into real nodes. It works row by row: it keeps the nodes it has made in a waiting line, and each node in the line takes the next two values of the list as its left and right child.

```python
def build(values):
    if not values:
        return None
    root = TreeNode(values[0])
    line = [root]
    head = 0
    i = 1
    while head < len(line) and i < len(values):
        node = line[head]
        head += 1
        if values[i] is not None:
            node.left = TreeNode(values[i])
            line.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            line.append(node.right)
        i += 1
    return root


tree = build([3, 9, 20, None, None, 15, 7])
assert tree.left.val == 9
assert tree.right.left.val == 15
assert tree.left.left is None
assert build([]) is None
```

```cpp
const int NIL = INT_MIN;  // stands for "no node" in a level-order list

TreeNode* build(const vector<int>& values) {
    if (values.empty()) return nullptr;
    TreeNode* root = new TreeNode(values[0]);
    vector<TreeNode*> line = {root};
    size_t head = 0, i = 1;
    while (head < line.size() && i < values.size()) {
        TreeNode* node = line[head++];
        if (values[i] != NIL) {
            node->left = new TreeNode(values[i]);
            line.push_back(node->left);
        }
        i++;
        if (i < values.size() && values[i] != NIL) {
            node->right = new TreeNode(values[i]);
            line.push_back(node->right);
        }
        i++;
    }
    return root;
}
```

We will use `build` in the examples of every chapter, so you can write `build([1, 2, 3])` and get a tree to play with.

## 1.3 Thinking with recursion

A **recursive** function is a function that calls itself on a smaller piece of the problem. For a tree, the smaller pieces are the two subtrees. To count the nodes of a tree, we can reason like this: the count for an empty tree is 0; otherwise it is 1 (for the root) plus the count of the left subtree plus the count of the right subtree. We do not need to think about how those two counts are found. We simply trust the function to do its job on the smaller trees.

Every recursive function needs a **base case**, the situation so simple that we answer directly without calling ourselves. For trees the base case is almost always "the node is `None`", which means "an empty tree".

```python
def count_nodes(root):
    if root is None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def count_leaves(root):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 1
    return count_leaves(root.left) + count_leaves(root.right)


t = build([3, 9, 20, None, None, 15, 7])
assert count_nodes(t) == 5
assert count_leaves(t) == 3
assert count_nodes(None) == 0
```

```cpp
int count_nodes(TreeNode* root) {
    if (root == nullptr) return 0;
    return 1 + count_nodes(root->left) + count_nodes(root->right);
}

int count_leaves(TreeNode* root) {
    if (root == nullptr) return 0;
    if (root->left == nullptr && root->right == nullptr) return 1;
    return count_leaves(root->left) + count_leaves(root->right);
}
```

Both functions visit every node exactly once, so the time is $O(n)$ for a tree with $n$ nodes. The recursion goes as deep as the height $h$ of the tree, so the extra memory is $O(h)$. For a well-spread tree $h$ is about $\log n$, but for a tree that is one long chain, $h = n$.

## 1.4 Check yourself

1. Which node of a tree has no parent, and what do we call a node with no children?
2. In the tree `[8, 3, 10, 1, 6, None, 14]`, what is the depth of the node `6`?
3. What is the usual base case of a recursive tree function?
4. Why does the number of nodes in a tree equal $1 +$ (nodes on the left) $+$ (nodes on the right)?

# Chapter 2. Depth-first traversals with recursion

## 2.1 Visiting every node

A **traversal** means visiting every node of the tree exactly once, in some order, and doing something at each visit (here, writing down the value). A list is easy to walk through, from the first element to the last. A tree has no single "next" element, so we need a rule that tells us where to go.

The first family of rules is **depth-first search**, or DFS: go as deep as possible along one branch, and only then come back and try the other branch. Think of exploring a maze by always taking the first unexplored corridor and backing up when you hit a dead end. For a tree, a DFS at a node does three things, in some order: handle the node itself, walk the whole left subtree, walk the whole right subtree. The left subtree always comes before the right one. The only choice is where "handle the node" goes, and that gives three famous orders.

```
        1
       / \
      2   3
     / \
    4   5
```

We will use this small tree in all the examples of this chapter.

## 2.2 Preorder: node first

In **preorder** you handle the node first, then the left subtree, then the right subtree ("pre" means before the children). On the tree above you write `1`, then you go left and handle the whole subtree of `2` (which gives `2, 4, 5`), then you go right (`3`). The result is `1, 2, 4, 5, 3`.

Preorder is the order in which you would copy a tree: you create a node before you create its children. It also puts the root first, a fact we will use later to rebuild trees.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build(values):
    if not values:
        return None
    root = TreeNode(values[0])
    line = [root]
    head = 0
    i = 1
    while head < len(line) and i < len(values):
        node = line[head]
        head += 1
        if values[i] is not None:
            node.left = TreeNode(values[i])
            line.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            line.append(node.right)
        i += 1
    return root


def preorder(root):
    out = []

    def visit(node):
        if node is None:
            return
        out.append(node.val)
        visit(node.left)
        visit(node.right)

    visit(root)
    return out


sample = build([1, 2, 3, 4, 5])
assert preorder(sample) == [1, 2, 4, 5, 3]
assert preorder(None) == []
```

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {}
};

const int NIL = INT_MIN;

TreeNode* build(const vector<int>& values) {
    if (values.empty()) return nullptr;
    TreeNode* root = new TreeNode(values[0]);
    vector<TreeNode*> line = {root};
    size_t head = 0, i = 1;
    while (head < line.size() && i < values.size()) {
        TreeNode* node = line[head++];
        if (values[i] != NIL) {
            node->left = new TreeNode(values[i]);
            line.push_back(node->left);
        }
        i++;
        if (i < values.size() && values[i] != NIL) {
            node->right = new TreeNode(values[i]);
            line.push_back(node->right);
        }
        i++;
    }
    return root;
}

void visit_pre(TreeNode* node, vector<int>& out) {
    if (node == nullptr) return;
    out.push_back(node->val);
    visit_pre(node->left, out);
    visit_pre(node->right, out);
}

vector<int> preorder(TreeNode* root) {
    vector<int> out;
    visit_pre(root, out);
    return out;
}
```

(The first part of that block is the same `TreeNode` and `build` as in Chapter 1, repeated so that this chapter stands on its own. We will repeat it at the start of each chapter and skip the explanation from now on.)

## 2.3 Inorder: node in the middle

In **inorder** you walk the whole left subtree first, then handle the node, then walk the right subtree ("in" means in between). On our tree, the left subtree of `1` gives `4, 2, 5`, then `1` itself, then the right subtree gives `3`. The result is `4, 2, 5, 1, 3`.

Inorder looks odd on this tree, but it has a beautiful meaning for the **binary search trees** of the next step: there it lists the values in sorted order.

```python
def inorder(root):
    out = []

    def visit(node):
        if node is None:
            return
        visit(node.left)
        out.append(node.val)
        visit(node.right)

    visit(root)
    return out


assert inorder(sample) == [4, 2, 5, 1, 3]
assert inorder(build([2, 1, 3])) == [1, 2, 3]
```

```cpp
void visit_in(TreeNode* node, vector<int>& out) {
    if (node == nullptr) return;
    visit_in(node->left, out);
    out.push_back(node->val);
    visit_in(node->right, out);
}

vector<int> inorder(TreeNode* root) {
    vector<int> out;
    visit_in(root, out);
    return out;
}
```

## 2.4 Postorder: node last

In **postorder** you walk both subtrees first and handle the node at the very end ("post" means after the children). On our tree: left subtree `4, 5, 2`, then right subtree `3`, then `1`. The result is `4, 5, 2, 3, 1`.

Postorder is the order to use when a node can only be finished once its children are finished. Deleting a tree is a good example: you free the children before the parent. Many of the later "answer flows up" problems (heights, sums, diameters) are secretly postorder.

```python
def postorder(root):
    out = []

    def visit(node):
        if node is None:
            return
        visit(node.left)
        visit(node.right)
        out.append(node.val)

    visit(root)
    return out


assert postorder(sample) == [4, 5, 2, 3, 1]
assert postorder(build([1, None, 2])) == [2, 1]
```

```cpp
void visit_post(TreeNode* node, vector<int>& out) {
    if (node == nullptr) return;
    visit_post(node->left, out);
    visit_post(node->right, out);
    out.push_back(node->val);
}

vector<int> postorder(TreeNode* root) {
    vector<int> out;
    visit_post(root, out);
    return out;
}
```

Notice that the three functions are identical except for the position of one line. That is the whole difference between the three orders. A handy way to remember: look at where the node itself sits compared with its two subtrees (pre = before, in = between, post = after).

## 2.5 Cost of the recursive walk

Every node is entered once and each of the three lines runs a constant number of times, so all three traversals take $O(n)$ time. The extra memory is the **call stack**, the pile of unfinished function calls the computer keeps. At any moment it holds one call per node on the path from the root to the node we are visiting, so it needs $O(h)$ space, where $h$ is the height.

This matters in practice. A tree that is one long chain of 100,000 nodes would make the recursion 100,000 calls deep, and many languages (Python in particular, with a default limit around 1,000) will crash. The next chapter shows how to walk the tree without recursion, using a stack that we manage ourselves.

## 2.6 Check yourself

1. Write the preorder, inorder and postorder of the tree `[1, None, 2, 3]` (root `1`, no left child, right child `2`, which has the left child `3`).
2. Which of the three orders always puts the root first, and which always puts it last?
3. What is the time cost of a traversal, and what decides the extra memory?
4. Why can a very deep tree break a recursive traversal in Python?

# Chapter 3. Traversals without recursion

## 3.1 A stack of our own

Recursion is a stack in disguise: each unfinished call waits on the call stack until the calls above it return. If we keep our own stack, a plain list where we `append` and `pop` at the end, we can do exactly the same walk with a loop. There is no recursion limit to worry about, and the idea is also good training for later problems.

The key picture is that the stack holds "work still to do". We always take the top item, which is the most recently added, so we dive deeper before coming back to older items. That is exactly depth-first behaviour.

## 3.2 Iterative preorder

For preorder, the stack holds nodes that are waiting to be visited. We start with the root. Then, repeatedly: pop a node, write its value, and push its two children. Which child should be pushed first? The stack gives back the last pushed item first, and we want to visit the left child before the right one, so we push the **right child first** and the **left child second**.

On the tree `[1, 2, 3, 4, 5]`: the stack is `[1]`; pop `1`, write 1, push `3` then `2`, giving `[3, 2]`; pop `2`, write 2, push `5` then `4`, giving `[3, 5, 4]`; pop `4`, write 4; pop `5`, write 5; pop `3`, write 3. The output is `1, 2, 4, 5, 3`, matching the recursive preorder. This is exactly the problem _Preorder Traversal_.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build(values):
    if not values:
        return None
    root = TreeNode(values[0])
    line = [root]
    head = 0
    i = 1
    while head < len(line) and i < len(values):
        node = line[head]
        head += 1
        if values[i] is not None:
            node.left = TreeNode(values[i])
            line.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            line.append(node.right)
        i += 1
    return root


def preorder_iterative(root):
    out = []
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out


sample = build([1, 2, 3, 4, 5])
assert preorder_iterative(sample) == [1, 2, 4, 5, 3]
assert preorder_iterative(None) == []
```

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {}
};

const int NIL = INT_MIN;

TreeNode* build(const vector<int>& values) {
    if (values.empty()) return nullptr;
    TreeNode* root = new TreeNode(values[0]);
    vector<TreeNode*> line = {root};
    size_t head = 0, i = 1;
    while (head < line.size() && i < values.size()) {
        TreeNode* node = line[head++];
        if (values[i] != NIL) {
            node->left = new TreeNode(values[i]);
            line.push_back(node->left);
        }
        i++;
        if (i < values.size() && values[i] != NIL) {
            node->right = new TreeNode(values[i]);
            line.push_back(node->right);
        }
        i++;
    }
    return root;
}

vector<int> preorder_iterative(TreeNode* root) {
    vector<int> out;
    vector<TreeNode*> stack;
    if (root) stack.push_back(root);
    while (!stack.empty()) {
        TreeNode* node = stack.back();
        stack.pop_back();
        out.push_back(node->val);
        if (node->right) stack.push_back(node->right);
        if (node->left) stack.push_back(node->left);
    }
    return out;
}
```

Each node is pushed and popped once, so the time is $O(n)$. The stack never holds more than one pending sibling per level plus the current path, which is $O(h)$ in a balanced tree and up to $O(n)$ for a tree shaped like a comb. The memory is on the heap, so there is no crash for deep trees.

## 3.3 Iterative inorder

Inorder is trickier, because a node must wait until its whole left subtree is done. The trick is to walk **left as far as possible**, pushing every node we pass, since each of them still has to be written later. When we cannot go left any more, we pop the top of the stack: that node has an empty (or finished) left side, so it is next in line. We write it, and then we move to its right child and repeat.

So the loop has a variable `cur` ("where am I?") and a stack ("who is waiting for me to come back?"). On `[1, 2, 3, 4, 5]`: from `1` walk left, pushing `1`, `2`, `4`. Pop `4`, write 4; its right is empty, so we pop again: `2`, write 2, and move to its right child `5`. Push `5`, nothing on its left, pop `5`, write 5. Pop `1`, write 1, move to `3`; push `3`, pop `3`, write 3. Output: `4, 2, 5, 1, 3`. This is exactly the problem _Inorder Traversal_.

```python
def inorder_iterative(root):
    out = []
    stack = []
    cur = root
    while cur is not None or stack:
        while cur is not None:        # dive left, remembering the way back
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()             # nothing more on the left
        out.append(cur.val)
        cur = cur.right               # now do the right side
    return out


assert inorder_iterative(sample) == [4, 2, 5, 1, 3]
assert inorder_iterative(build([2, 1, 3])) == [1, 2, 3]
assert inorder_iterative(None) == []
```

```cpp
vector<int> inorder_iterative(TreeNode* root) {
    vector<int> out;
    vector<TreeNode*> stack;
    TreeNode* cur = root;
    while (cur != nullptr || !stack.empty()) {
        while (cur != nullptr) {
            stack.push_back(cur);
            cur = cur->left;
        }
        cur = stack.back();
        stack.pop_back();
        out.push_back(cur->val);
        cur = cur->right;
    }
    return out;
}
```

Time is $O(n)$ (each node is pushed once and popped once) and extra space is $O(h)$. This pattern, "go left, pop, go right", is worth remembering because the binary-search-tree step uses it again and again.

## 3.4 Iterative postorder

Postorder is the hardest to do with one stack, because a node must be written only after both of its subtrees, so we would have to remember whether we are returning from the left or the right. There is a neat shortcut. The reverse of postorder (left, right, node) reads (node, right, left). That looks like preorder with the two children swapped! So we run the preorder loop, push the left child first and the right child second, so that right is visited first, and then reverse the final list.

On `[1, 2, 3, 4, 5]` this loop writes `1, 3, 2, 5, 4`. Reversed, that is `4, 5, 2, 3, 1`, which is the postorder. This is exactly the problem _Postorder Traversal_.

```python
def postorder_iterative(root):
    out = []
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.val)          # order written: node, right, left
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    out.reverse()                     # becomes: left, right, node
    return out


assert postorder_iterative(sample) == [4, 5, 2, 3, 1]
assert postorder_iterative(build([1, None, 2, 3])) == [3, 2, 1]
assert postorder_iterative(None) == []
```

```cpp
vector<int> postorder_iterative(TreeNode* root) {
    vector<int> out;
    vector<TreeNode*> stack;
    if (root) stack.push_back(root);
    while (!stack.empty()) {
        TreeNode* node = stack.back();
        stack.pop_back();
        out.push_back(node->val);
        if (node->left) stack.push_back(node->left);
        if (node->right) stack.push_back(node->right);
    }
    reverse(out.begin(), out.end());
    return out;
}
```

Time is $O(n)$ and space is $O(n)$ here (the answer list is built before reversing; the stack itself is $O(h)$). There are also one-stack versions that remember the last node written, but this reverse trick is short and easy to get right under pressure.

## 3.5 Check yourself

1. In iterative preorder, why do we push the right child before the left child?
2. In iterative inorder, what does the stack remember?
3. What does postorder look like when read backwards?
4. What do we gain by using our own stack instead of recursion?

# Chapter 4. Level by level with a queue

## 4.1 Breadth-first search

DFS dives deep. The other classic way to walk a tree is **breadth-first search**, or BFS: visit the root, then all nodes one step below it, then all nodes two steps below, and so on, one **level** (row) at a time. It is like ripples spreading from a stone dropped in water.

To do this we need a **queue**, a waiting line where new items join at the back and items leave from the front (first in, first out). We start with the root in the queue. Then, repeatedly: take the front node, handle it, and put its children at the back. Because children join behind everything already waiting, a whole level is finished before the next one starts. In Python the handy queue is `collections.deque`; in C++ it is `queue`.

## 4.2 Level order, row by row

Many problems want the values **grouped by level**: a list of lists, one inside list per row. We can get the grouping with one small trick. At the start of each round of the loop, the queue contains exactly the nodes of one level, so we note its length `count` and handle exactly `count` nodes. The children added during that round form the next level.

For `[3, 9, 20, None, None, 15, 7]` the rounds give `[3]`, then `[9, 20]`, then `[15, 7]`. This is exactly the problem _Level Order Traversal_.

```python
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build(values):
    if not values:
        return None
    root = TreeNode(values[0])
    line = [root]
    head = 0
    i = 1
    while head < len(line) and i < len(values):
        node = line[head]
        head += 1
        if values[i] is not None:
            node.left = TreeNode(values[i])
            line.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            line.append(node.right)
        i += 1
    return root


def level_order(root):
    result = []
    if root is None:
        return result
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):       # exactly one level
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result


assert level_order(build([3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]]
assert level_order(build([1])) == [[1]]
assert level_order(None) == []
```

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {}
};

const int NIL = INT_MIN;

TreeNode* build(const vector<int>& values) {
    if (values.empty()) return nullptr;
    TreeNode* root = new TreeNode(values[0]);
    vector<TreeNode*> line = {root};
    size_t head = 0, i = 1;
    while (head < line.size() && i < values.size()) {
        TreeNode* node = line[head++];
        if (values[i] != NIL) {
            node->left = new TreeNode(values[i]);
            line.push_back(node->left);
        }
        i++;
        if (i < values.size() && values[i] != NIL) {
            node->right = new TreeNode(values[i]);
            line.push_back(node->right);
        }
        i++;
    }
    return root;
}

vector<vector<int>> level_order(TreeNode* root) {
    vector<vector<int>> result;
    if (root == nullptr) return result;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        int count = q.size();
        vector<int> level;
        for (int i = 0; i < count; i++) {
            TreeNode* node = q.front();
            q.pop();
            level.push_back(node->val);
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
        result.push_back(level);
    }
    return result;
}
```

Every node enters and leaves the queue once, so the time is $O(n)$. The queue holds at most one level at a time, so the space is $O(w)$ where $w$ is the widest level, which is at most $O(n)$.

## 4.3 Zigzag level order

In a **zigzag** order, the first row is read left to right, the second right to left, the third left to right again, and so on. Nothing about the walk itself changes: we still need the levels in normal order from the queue. We only reverse every second row afterwards. Rows with an odd position (counting from 0) are the ones to flip.

For `[3, 9, 20, None, None, 15, 7]` the normal rows are `[3]`, `[9, 20]`, `[15, 7]`, and flipping the middle one gives `[3]`, `[20, 9]`, `[15, 7]`. This is exactly the problem _Zigzag Level Order_.

```python
def zigzag_level_order(root):
    levels = level_order(root)
    for i in range(1, len(levels), 2):
        levels[i].reverse()
    return levels


assert zigzag_level_order(build([3, 9, 20, None, None, 15, 7])) == [[3], [20, 9], [15, 7]]
assert zigzag_level_order(build([1, 2, 3, 4, 5, 6, 7])) == [[1], [3, 2], [4, 5, 6, 7]]
```

```cpp
vector<vector<int>> zigzag_level_order(TreeNode* root) {
    vector<vector<int>> levels = level_order(root);
    for (size_t i = 1; i < levels.size(); i += 2) {
        reverse(levels[i].begin(), levels[i].end());
    }
    return levels;
}
```

The extra reversing costs $O(n)$ in total, so the whole thing is still $O(n)$ time and $O(w)$ space.

## 4.4 The right side view

Imagine standing to the right of the tree and looking at it. At each level you can see only the **rightmost** node of that row, because anything to its left is hidden behind it. So the answer is "the last value of every level".

With the level-order code this is just the last value of each row. There is also a short depth-first way, which is a nice contrast. Walk the tree visiting the **right child before the left**, and carry the current depth with you. The first time you reach a new depth, that node is the rightmost one of its row, so record it. If the right side has no node at some depth, the left side's node at that depth is the first one seen, and it is correctly recorded.

For `[1, 2, 3, None, 5, None, 4]` the view is `[1, 3, 4]`. This is exactly the problem _Right Side View_.

```python
def right_side_view(root):
    view = []

    def go(node, depth):
        if node is None:
            return
        if depth == len(view):        # first node seen at this depth
            view.append(node.val)
        go(node.right, depth + 1)     # right first
        go(node.left, depth + 1)

    go(root, 0)
    return view


assert right_side_view(build([1, 2, 3, None, 5, None, 4])) == [1, 3, 4]
assert right_side_view(build([1, 2, 3, 4])) == [1, 3, 4]
assert right_side_view(None) == []
```

```cpp
void go_right_view(TreeNode* node, int depth, vector<int>& view) {
    if (node == nullptr) return;
    if (depth == (int)view.size()) view.push_back(node->val);
    go_right_view(node->right, depth + 1, view);
    go_right_view(node->left, depth + 1, view);
}

vector<int> right_side_view(TreeNode* root) {
    vector<int> view;
    go_right_view(root, 0, view);
    return view;
}
```

Notice the second example: in `[1, 2, 3, 4]` the node `3` has no children, so at depth 2 nothing hides the node `4`, and it shows up even though it is on the left. The time is $O(n)$ and the space is $O(h)$.

## 4.5 Vertical order with columns

Now give every node a **column** number. The root is in column 0, a left child is one column to the left (the parent's column minus 1) and a right child one column to the right (plus 1). Draw vertical lines through the columns and read each line from top to bottom. That is the **vertical order traversal**.

```
        3          column:  -1  0  1  2
       / \                   9  3  20  7
      9   20                    15
         /  \
        15   7
```

The node `15` is the left child of `20` (column 1), so it lands in column 0, right under `3`. The answer is `[[9], [3, 15], [20], [7]]`.

We need every node's column and its row (depth). BFS gives us the rows for free, and we carry the column along in the queue together with the row. Then we collect triples `(column, row, value)`, sort them, and cut the sorted list into groups by column. Sorting by `(column, row, value)` is exactly what the rules ask for: left to right across columns, top to bottom inside a column, and smaller value first when two nodes share a row and column. This is exactly the problem _Vertical Order Traversal_.

```python
def vertical_order(root):
    if root is None:
        return []
    cells = []                                  # (column, row, value)
    queue = deque([(root, 0, 0)])
    while queue:
        node, col, row = queue.popleft()
        cells.append((col, row, node.val))
        if node.left:
            queue.append((node.left, col - 1, row + 1))
        if node.right:
            queue.append((node.right, col + 1, row + 1))
    cells.sort()
    result = []
    last_col = None
    for col, row, val in cells:
        if col != last_col:
            result.append([])
            last_col = col
        result[-1].append(val)
    return result


assert vertical_order(build([3, 9, 20, None, None, 15, 7])) == [[9], [3, 15], [20], [7]]
assert vertical_order(build([1, 2, 3, 4, 6, 5, 7])) == [[4], [2], [1, 5, 6], [3], [7]]
```

```cpp
vector<vector<int>> vertical_order(TreeNode* root) {
    vector<vector<int>> result;
    if (root == nullptr) return result;
    vector<tuple<int, int, int>> cells;      // (column, row, value)
    queue<tuple<TreeNode*, int, int>> q;
    q.push({root, 0, 0});
    while (!q.empty()) {
        auto [node, col, row] = q.front();
        q.pop();
        cells.push_back({col, row, node->val});
        if (node->left) q.push({node->left, col - 1, row + 1});
        if (node->right) q.push({node->right, col + 1, row + 1});
    }
    sort(cells.begin(), cells.end());
    bool first = true;
    int last_col = 0;
    for (auto& [col, row, val] : cells) {
        if (first || col != last_col) {
            result.push_back({});
            last_col = col;
            first = false;
        }
        result.back().push_back(val);
    }
    return result;
}
```

In the second example, `5` and `6` both sit in column 0 and row 2, so the smaller value comes first: `[1, 5, 6]`. The BFS is $O(n)$ and the sort dominates, so the total time is $O(n \log n)$ and the space is $O(n)$.

## 4.6 Check yourself

1. Why does a queue make us visit a whole level before the next one?
2. How does the loop know where one level ends and the next begins?
3. How do we turn the normal level order into a zigzag order?
4. In vertical order, what is the column of the left child of a node in column $c$?

# Chapter 5. Letting the children answer

## 5.1 The recipe

Most tree questions can be solved with one calm way of thinking. Suppose you have to compute something for a whole tree. Pretend that someone has already solved the question for the **left subtree** and for the **right subtree**. Your only job is to combine those two answers with the root. If you can write that combination, you are done, plus one base case for the empty tree.

The recipe has three steps. First, decide what the function returns for `None`. Second, call the function on `root.left` and `root.right` and trust the answers. Third, combine them with the current node and return. The questions of this chapter are all small versions of this recipe, and the shape stays the same for hard problems later.

## 5.2 Maximum depth

The **maximum depth** is the number of nodes on the longest path from the root down to a leaf. For an empty tree it is 0. Otherwise the longest path goes through the deeper child: take the larger of the two child answers and add 1 for the current node. This is exactly the problem _Maximum Depth_.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build(values):
    if not values:
        return None
    root = TreeNode(values[0])
    line = [root]
    head = 0
    i = 1
    while head < len(line) and i < len(values):
        node = line[head]
        head += 1
        if values[i] is not None:
            node.left = TreeNode(values[i])
            line.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            line.append(node.right)
        i += 1
    return root


def to_list(root):
    out = []
    line = [root]
    head = 0
    while head < len(line):
        node = line[head]
        head += 1
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            line.append(node.left)
            line.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def max_depth(root):
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


assert max_depth(build([3, 9, 20, None, None, 15, 7])) == 3
assert max_depth(build([1, None, 2])) == 2
assert max_depth(None) == 0
```

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {}
};

const int NIL = INT_MIN;

TreeNode* build(const vector<int>& values) {
    if (values.empty()) return nullptr;
    TreeNode* root = new TreeNode(values[0]);
    vector<TreeNode*> line = {root};
    size_t head = 0, i = 1;
    while (head < line.size() && i < values.size()) {
        TreeNode* node = line[head++];
        if (values[i] != NIL) {
            node->left = new TreeNode(values[i]);
            line.push_back(node->left);
        }
        i++;
        if (i < values.size() && values[i] != NIL) {
            node->right = new TreeNode(values[i]);
            line.push_back(node->right);
        }
        i++;
    }
    return root;
}

vector<int> to_list(TreeNode* root) {
    vector<int> out;
    vector<TreeNode*> line = {root};
    size_t head = 0;
    while (head < line.size()) {
        TreeNode* node = line[head++];
        if (node == nullptr) {
            out.push_back(NIL);
        } else {
            out.push_back(node->val);
            line.push_back(node->left);
            line.push_back(node->right);
        }
    }
    while (!out.empty() && out.back() == NIL) out.pop_back();
    return out;
}

int max_depth(TreeNode* root) {
    if (root == nullptr) return 0;
    return 1 + max(max_depth(root->left), max_depth(root->right));
}
```

Every node is looked at once, so the time is $O(n)$, and the space is the call-stack depth, $O(h)$. (`to_list`, the reverse of `build`, is a helper we use to check results that are trees.)

## 5.3 Minimum depth

The **minimum depth** is the number of nodes on the shortest path from the root down to a **leaf**. It is tempting to copy the last function and replace `max` by `min`, but that is a classic trap. Take the tree `[2, None, 3]`: the root has an empty left side. Taking `min` would compare 0 (the empty left) with 1, and answer 1. But the root `2` is not a leaf, so a path must continue to the leaf `3`, and the correct answer is 2.

The fix: if one child is missing, the only way down is through the other child, so we must not let the empty side win. We only take the `min` when both children exist. This is exactly the problem _Minimum Depth_.

```python
def min_depth(root):
    if root is None:
        return 0
    if root.left is None:
        return 1 + min_depth(root.right)
    if root.right is None:
        return 1 + min_depth(root.left)
    return 1 + min(min_depth(root.left), min_depth(root.right))


assert min_depth(build([3, 9, 20, None, None, 15, 7])) == 2
assert min_depth(build([2, None, 3, None, 4])) == 3
assert min_depth(None) == 0
```

```cpp
int min_depth(TreeNode* root) {
    if (root == nullptr) return 0;
    if (root->left == nullptr) return 1 + min_depth(root->right);
    if (root->right == nullptr) return 1 + min_depth(root->left);
    return 1 + min(min_depth(root->left), min_depth(root->right));
}
```

The time is $O(n)$ and the space is $O(h)$. (A BFS from Chapter 4 can stop at the first leaf it sees, which can be faster on wide trees, but the recursion is shorter to write.)

## 5.4 Same tree and symmetric tree

Comparing two trees is a recursion on **two nodes at once**. Two trees are the same when both are empty, or when both roots hold the same value and the left subtrees are the same and the right subtrees are the same. If exactly one of them is empty, they differ. This is exactly the problem _Same Tree_.

A tree is **symmetric** (a mirror image of itself) when its left half is the mirror of its right half. Two trees are mirrors of each other when their roots are equal and the **left of the first mirrors the right of the second**, and the **right of the first mirrors the left of the second**. So the same two-node recursion works, with the children crossed. We start by asking whether the left subtree and right subtree of the root are mirrors. This is exactly the problem _Symmetric Tree_.

```python
def is_same_tree(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.val == b.val and is_same_tree(a.left, b.left) and is_same_tree(a.right, b.right)


def is_mirror(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.val == b.val and is_mirror(a.left, b.right) and is_mirror(a.right, b.left)


def is_symmetric(root):
    if root is None:
        return True
    return is_mirror(root.left, root.right)


assert is_same_tree(build([1, 2, 3]), build([1, 2, 3]))
assert not is_same_tree(build([1, 2]), build([1, None, 2]))
assert is_symmetric(build([1, 2, 2, 3, 4, 4, 3]))
assert not is_symmetric(build([1, 2, 2, None, 3, None, 3]))
```

```cpp
bool is_same_tree(TreeNode* a, TreeNode* b) {
    if (a == nullptr && b == nullptr) return true;
    if (a == nullptr || b == nullptr) return false;
    return a->val == b->val && is_same_tree(a->left, b->left) && is_same_tree(a->right, b->right);
}

bool is_mirror(TreeNode* a, TreeNode* b) {
    if (a == nullptr && b == nullptr) return true;
    if (a == nullptr || b == nullptr) return false;
    return a->val == b->val && is_mirror(a->left, b->right) && is_mirror(a->right, b->left);
}

bool is_symmetric(TreeNode* root) {
    if (root == nullptr) return true;
    return is_mirror(root->left, root->right);
}
```

Both take $O(n)$ time in the worst case and $O(h)$ space. In the last assert, the tree `[1, 2, 2, None, 3, None, 3]` is not symmetric: both `2`s have their child on the right side, but a mirror would need one child on the left and one on the right.

## 5.5 Inverting a tree

To **invert** (flip) a tree is to swap the left and right child of every node, which makes a mirror image. With the recipe: invert the left subtree, invert the right subtree, then swap the two results at the current node. The recursion can even do the swap first; the order does not matter as long as every node gets swapped exactly once. This is exactly the problem _Invert a Binary Tree_.

```python
def invert_tree(root):
    if root is None:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


assert to_list(invert_tree(build([4, 2, 7, 1, 3, 6, 9]))) == [4, 7, 2, 9, 6, 3, 1]
assert to_list(invert_tree(build([1, 2]))) == [1, None, 2]
assert invert_tree(None) is None
```

```cpp
TreeNode* invert_tree(TreeNode* root) {
    if (root == nullptr) return nullptr;
    TreeNode* left = invert_tree(root->left);
    TreeNode* right = invert_tree(root->right);
    root->left = right;
    root->right = left;
    return root;
}
```

The time is $O(n)$ and the space is $O(h)$.

## 5.6 Check yourself

1. What does the recipe say to do with the answers for the two subtrees?
2. Why is `1 + min(min_depth(left), min_depth(right))` wrong when one child is empty?
3. In the mirror test, which children of the two nodes are compared with each other?
4. What is the minimum depth and the maximum depth of a tree with only a root?

# Chapter 6. Carrying information down

## 6.1 Two directions of information

In Chapter 5 the answers travelled **up**: each call returned a value to its parent. Sometimes the information is needed in the other direction. To know whether the current node is the end of a good path, a node must know what happened **above** it, such as the sum so far. We handle this by giving the function an extra **parameter** that the parent fills in when it calls the child. Information goes down through parameters and comes back up through return values, and many solutions use both.

## 6.2 Root-to-leaf path sum

Question: is there a path from the root down to a **leaf** whose values add up to `target`? Instead of adding values up and comparing at the end, we count down. At each node we subtract its value from the target, and pass the **remaining** amount to the children. At a leaf, the path works if nothing remains, that is, the remaining amount is 0 after subtracting the leaf's own value.

Take `[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]` and target 22. At the root the remaining amount becomes 17, at `4` it becomes 13, at `11` it becomes 2, and at the leaf `2` it becomes 0. A path exists. This is exactly the problem _Root-to-Leaf Path Sum_.

Be careful about two details. The path must end at a **leaf**, not at any node: in `[1, 2]` with target 1, the root alone has the right sum but it is not a leaf, so the answer is `False`. And an empty tree has no path, even when the target is 0.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build(values):
    if not values:
        return None
    root = TreeNode(values[0])
    line = [root]
    head = 0
    i = 1
    while head < len(line) and i < len(values):
        node = line[head]
        head += 1
        if values[i] is not None:
            node.left = TreeNode(values[i])
            line.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            line.append(node.right)
        i += 1
    return root


def has_path_sum(root, target):
    if root is None:
        return False
    remaining = target - root.val
    if root.left is None and root.right is None:
        return remaining == 0
    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)


big = build([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
assert has_path_sum(big, 22)
assert not has_path_sum(big, 5)
assert not has_path_sum(build([1, 2]), 1)
assert not has_path_sum(None, 0)
```

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {}
};

const int NIL = INT_MIN;

TreeNode* build(const vector<int>& values) {
    if (values.empty()) return nullptr;
    TreeNode* root = new TreeNode(values[0]);
    vector<TreeNode*> line = {root};
    size_t head = 0, i = 1;
    while (head < line.size() && i < values.size()) {
        TreeNode* node = line[head++];
        if (values[i] != NIL) {
            node->left = new TreeNode(values[i]);
            line.push_back(node->left);
        }
        i++;
        if (i < values.size() && values[i] != NIL) {
            node->right = new TreeNode(values[i]);
            line.push_back(node->right);
        }
        i++;
    }
    return root;
}

bool has_path_sum(TreeNode* root, int target) {
    if (root == nullptr) return false;
    int remaining = target - root->val;
    if (root->left == nullptr && root->right == nullptr) return remaining == 0;
    return has_path_sum(root->left, remaining) || has_path_sum(root->right, remaining);
}
```

The time is $O(n)$ (we may have to try every path) and the space is $O(h)$.

## 6.3 Listing all root-to-leaf paths

Now we want every root-to-leaf path written out as text like `"1->2->5"`. We carry the **path so far** downwards. At each node we add its value to the path; if the node is a leaf, we write the path down in the answer; otherwise we continue into the children.

Here is the new idea: **backtracking**. We use one shared list `path` for the whole walk instead of making a fresh copy at every call (copying would waste time). When we have finished with a node, we remove its value from the list so that the parent can use the same list for its other child. "Add on the way in, remove on the way out" keeps the list equal to the real path at all times.

The order of the answer is left to right, because we always go into the left child first. For `[1, 2, 3, None, 5]` the walk adds `1`, `2`, `5` and writes `1->2->5`, backs out to `1`, adds `3`, writes `1->3`. This is exactly the problem _All Root-to-Leaf Paths_.

```python
def all_paths(root):
    result = []
    path = []

    def go(node):
        if node is None:
            return
        path.append(str(node.val))
        if node.left is None and node.right is None:
            result.append("->".join(path))
        else:
            go(node.left)
            go(node.right)
        path.pop()                      # backtrack

    go(root)
    return result


assert all_paths(build([1, 2, 3, None, 5])) == ["1->2->5", "1->3"]
assert all_paths(build([7])) == ["7"]
assert all_paths(None) == []
```

```cpp
void go_paths(TreeNode* node, vector<int>& path, vector<string>& result) {
    if (node == nullptr) return;
    path.push_back(node->val);
    if (node->left == nullptr && node->right == nullptr) {
        string text;
        for (size_t i = 0; i < path.size(); i++) {
            if (i > 0) text += "->";
            text += to_string(path[i]);
        }
        result.push_back(text);
    } else {
        go_paths(node->left, path, result);
        go_paths(node->right, path, result);
    }
    path.pop_back();                    // backtrack
}

vector<string> all_paths(TreeNode* root) {
    vector<string> result;
    vector<int> path;
    go_paths(root, path, result);
    return result;
}
```

If the tree has $n$ nodes and $L$ leaves, each path has at most $h + 1$ values, so writing the answer costs $O(L \cdot h)$ and the walk costs $O(n)$. The same backtracking idea also solves "find the path with a given sum" and many other path-listing problems.

## 6.4 Check yourself

1. In the path-sum code, what do we pass down, and what comes back up?
2. Why must the check for the target happen only at leaves?
3. What does `path.pop()` do and why is it needed?
4. Name one difference between passing information down and returning it up.

# Chapter 7. Combining answers going up

## 7.1 A return value and a side answer

Some questions cannot be answered by the recipe of Chapter 5 alone, because the best answer for a node is not the best answer built from the best children. The classic example: the longest path in a tree may bend at some node in the middle and use both of its sides, but a path that we hand to the parent must be a straight line that can still be extended.

The cure is to keep two different things apart. The function returns to its parent the **best straight line going down** from this node (usually a height). Separately, it uses the two values it received from its children to update a global "best answer so far" in a variable outside the recursion. The returned value is what the parent needs; the recorded value is what the whole question needs.

## 7.2 Diameter of a tree

The **diameter** is the number of edges in the longest path between any two nodes, which does not have to pass through the root. Look at any path: it has a highest node, the one where it turns. Through a node whose left side reaches down $l$ edges and whose right side reaches down $r$ edges, the longest bent path has $l + r$ edges. So for each node we compute these two heights and record $l + r$; the answer is the maximum over all nodes.

In terms of node counts: a node whose left subtree has height `lh` and right subtree has height `rh` (counting nodes, so empty is 0) gets a bent path of `lh + rh` edges. The function returns `1 + max(lh, rh)` to the parent.

On `[1, 2, 3, 4, 5]`: node `4` and `5` give 0; node `2` has heights 1 and 1, so it records 2 and returns 2; node `3` returns 1; the root sees 2 and 1, so it records 3. The answer is 3 (the path `4, 2, 1, 3`). This is exactly the problem _Diameter of a Binary Tree_.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build(values):
    if not values:
        return None
    root = TreeNode(values[0])
    line = [root]
    head = 0
    i = 1
    while head < len(line) and i < len(values):
        node = line[head]
        head += 1
        if values[i] is not None:
            node.left = TreeNode(values[i])
            line.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            line.append(node.right)
        i += 1
    return root


def diameter(root):
    best = 0

    def height(node):
        nonlocal best
        if node is None:
            return 0
        lh = height(node.left)
        rh = height(node.right)
        best = max(best, lh + rh)         # a path bending at this node
        return 1 + max(lh, rh)            # a straight path for the parent

    height(root)
    return best


assert diameter(build([1, 2, 3, 4, 5])) == 3
assert diameter(build([1])) == 0
assert diameter(build([1, 2, None, 3, None, 4])) == 3
```

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {}
};

const int NIL = INT_MIN;

TreeNode* build(const vector<int>& values) {
    if (values.empty()) return nullptr;
    TreeNode* root = new TreeNode(values[0]);
    vector<TreeNode*> line = {root};
    size_t head = 0, i = 1;
    while (head < line.size() && i < values.size()) {
        TreeNode* node = line[head++];
        if (values[i] != NIL) {
            node->left = new TreeNode(values[i]);
            line.push_back(node->left);
        }
        i++;
        if (i < values.size() && values[i] != NIL) {
            node->right = new TreeNode(values[i]);
            line.push_back(node->right);
        }
        i++;
    }
    return root;
}

int diameter_height(TreeNode* node, int& best) {
    if (node == nullptr) return 0;
    int lh = diameter_height(node->left, best);
    int rh = diameter_height(node->right, best);
    best = max(best, lh + rh);
    return 1 + max(lh, rh);
}

int diameter(TreeNode* root) {
    int best = 0;
    diameter_height(root, best);
    return best;
}
```

One pass over the tree gives $O(n)$ time and $O(h)$ space. A common slow mistake is to compute the height of both sides again at every node, which costs $O(n^2)$ on a chain.

## 7.3 Balanced tree check

A tree is **height-balanced** when, at every node, the heights of the left and right subtrees differ by at most 1. The slow way asks for the height of both sides at each node and compares, which repeats a lot of work. The fast way is to compute the height and check the balance in the same pass.

The trick is a **sentinel**, a special return value that means "something is wrong". Let the function return the height as usual, but return `-1` when the subtree is unbalanced. When a node receives `-1` from a child it immediately passes `-1` upward without looking further. If both children are fine, it compares their heights, and returns `-1` when they differ by more than 1, and `1 + max(lh, rh)` otherwise. This is exactly the problem _Balanced Binary Tree_.

```python
def is_balanced(root):
    def height(node):
        if node is None:
            return 0
        lh = height(node.left)
        if lh == -1:
            return -1
        rh = height(node.right)
        if rh == -1:
            return -1
        if abs(lh - rh) > 1:
            return -1
        return 1 + max(lh, rh)

    return height(root) != -1


assert is_balanced(build([3, 9, 20, None, None, 15, 7]))
assert not is_balanced(build([1, 2, 2, 3, 3, None, None, 4, 4]))
assert is_balanced(None)
```

```cpp
int balanced_height(TreeNode* node) {
    if (node == nullptr) return 0;
    int lh = balanced_height(node->left);
    if (lh == -1) return -1;
    int rh = balanced_height(node->right);
    if (rh == -1) return -1;
    if (abs(lh - rh) > 1) return -1;
    return 1 + max(lh, rh);
}

bool is_balanced(TreeNode* root) {
    return balanced_height(root) != -1;
}
```

Each node is visited once, so the time is $O(n)$, and the space is $O(h)$.

## 7.4 Lowest common ancestor

Two nodes `p` and `q` have many common ancestors (the root is always one). The **lowest common ancestor**, or LCA, is the one farthest from the root, that is, the lowest node that has both `p` and `q` in its subtree. A node counts as being in its own subtree, so if `p` is above `q`, then `p` itself is the answer.

Let the function answer the question: "in this subtree, is there `p`, `q`, or an LCA?" It returns a node or `None`. At a node: if it is `None`, return `None`. If it is `p` or `q`, return it (we found one, and nothing below can be better, since the other one, if it is below, makes this node the LCA anyway). Otherwise ask both children. If **both** come back with something, then `p` and `q` are on different sides of this node, so this node is the LCA. If only one side comes back with something, pass it upward unchanged: it is either one of the nodes or the LCA already found.

On `[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]`, for `p = 5, q = 1` the root `3` hears from both sides, so the answer is `3`. For `p = 5, q = 4`, the node `5` is found first and returned; the right side returns nothing, so the answer is `5`. This is exactly the problem _Lowest Common Ancestor_.

```python
def lowest_common_ancestor(root, p, q):
    if root is None:
        return None
    if root.val == p or root.val == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left is not None and right is not None:
        return root
    return left if left is not None else right


tree = build([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
assert lowest_common_ancestor(tree, 5, 1).val == 3
assert lowest_common_ancestor(tree, 5, 4).val == 5
assert lowest_common_ancestor(tree, 7, 4).val == 2
```

```cpp
TreeNode* lowest_common_ancestor(TreeNode* root, int p, int q) {
    if (root == nullptr) return nullptr;
    if (root->val == p || root->val == q) return root;
    TreeNode* left = lowest_common_ancestor(root->left, p, q);
    TreeNode* right = lowest_common_ancestor(root->right, p, q);
    if (left != nullptr && right != nullptr) return root;
    return left != nullptr ? left : right;
}
```

The time is $O(n)$ and the space is $O(h)$.

## 7.5 Maximum path sum

Now the hardest of this family. A **path** goes along parent-child links, starts and ends anywhere and uses each node once, and we want the largest sum of values on it. Values can be negative, so a longer path is not always better.

It is the diameter idea with sums instead of lengths. For each node we want the best straight path going **down** from it, called its **gain**. A negative gain is useless to extend into, so a node ignores a child whose gain is negative (it uses `max(gain, 0)`). The best path that bends at this node is its value plus the left gain plus the right gain; we record that. The function returns to the parent only a straight line: the node's value plus the better of the two gains.

On `[-10, 9, 20, None, None, 15, 7]`: the node `20` has gains 15 and 7, so it records $20 + 15 + 7 = 42$ and returns $20 + 15 = 35$. The root has gains 9 and 35, and records $-10 + 9 + 35 = 34$, which is less than 42. The answer is 42. A tree with a single node `-3` has answer `-3`, which is why the starting value of "best" must be very small and not 0. This is exactly the problem _Maximum Path Sum_.

```python
def max_path_sum(root):
    best = float("-inf")

    def gain(node):
        nonlocal best
        if node is None:
            return 0
        left = max(gain(node.left), 0)
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)    # bend at this node
        return node.val + max(left, right)           # straight line for the parent

    gain(root)
    return best


assert max_path_sum(build([-10, 9, 20, None, None, 15, 7])) == 42
assert max_path_sum(build([-3])) == -3
assert max_path_sum(build([1, 2, 3])) == 6
assert max_path_sum(build([2, -1])) == 2
```

```cpp
int path_gain(TreeNode* node, int& best) {
    if (node == nullptr) return 0;
    int left = max(path_gain(node->left, best), 0);
    int right = max(path_gain(node->right, best), 0);
    best = max(best, node->val + left + right);
    return node->val + max(left, right);
}

int max_path_sum(TreeNode* root) {
    int best = INT_MIN;
    path_gain(root, best);
    return best;
}
```

The time is $O(n)$ and the space is $O(h)$. If the values can be very large, use 64-bit integers (`long long`) in C++ to avoid overflow.

## 7.6 Check yourself

1. In the diameter code, which value is returned to the parent and which value is only recorded?
2. Why does the balanced check return `-1` instead of a normal height when something is wrong?
3. When does the LCA code return the current node because both children answered?
4. Why does the maximum path sum use `max(gain, 0)` for each child?

# Chapter 8. Building and reshaping trees

## 8.1 Why two traversals?

A single traversal list does not describe a tree uniquely: the trees `[1, 2]` and `[1, None, 2]` both have the preorder `1, 2`. But if we know the **preorder** and the **inorder** of a tree whose values are all different, then the tree is determined.

The reason is that the two orders give different information. Preorder tells us the **root** first (its very first value). Inorder tells us how the rest splits into **left** and **right**: everything written before the root in the inorder belongs to the left subtree, and everything after it to the right subtree.

Take preorder `[3, 9, 20, 15, 7]` and inorder `[9, 3, 15, 20, 7]`. The first preorder value, `3`, is the root. In the inorder list `3` sits at position 1, so `[9]` is the left subtree and `[15, 20, 7]` is the right subtree. Now repeat on each part: the next preorder value is `9`, the root of the left part, which has no children. After that comes `20`, the root of the right part, and in the inorder `[15, 20, 7]` it has `15` on its left and `7` on its right. We recover `[3, 9, 20, None, None, 15, 7]`.

## 8.2 Building from preorder and inorder

In code we keep a pointer `pos` that moves along the preorder list and always points to the next root to be used. A recursive helper builds the tree for a range of the inorder list. It takes `preorder[pos]` as the root, finds the root's position in the inorder range, builds the left subtree from the part before it, then the right subtree from the part after it. The **order of the calls matters**: the left subtree must be built first, because in the preorder the left subtree comes before the right one.

To avoid searching the inorder list again and again, we first make a dictionary from each value to its inorder position. The search then costs $O(1)$. This is exactly the problem _Build a Tree From Preorder and Inorder_.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def to_list(root):
    out = []
    line = [root]
    head = 0
    while head < len(line):
        node = line[head]
        head += 1
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            line.append(node.left)
            line.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def build_tree(preorder, inorder):
    index_of = {v: i for i, v in enumerate(inorder)}
    pos = 0

    def build_range(lo, hi):            # builds from inorder[lo:hi]
        nonlocal pos
        if lo >= hi:
            return None
        val = preorder[pos]
        pos += 1
        mid = index_of[val]
        node = TreeNode(val)
        node.left = build_range(lo, mid)
        node.right = build_range(mid + 1, hi)
        return node

    return build_range(0, len(inorder))


result = build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
assert to_list(result) == [3, 9, 20, None, None, 15, 7]
assert to_list(build_tree([1, 2], [2, 1])) == [1, 2]
assert build_tree([], []) is None
```

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {}
};

TreeNode* build_range(const vector<int>& preorder, unordered_map<int, int>& index_of,
                      int& pos, int lo, int hi) {
    if (lo >= hi) return nullptr;
    int val = preorder[pos++];
    int mid = index_of[val];
    TreeNode* node = new TreeNode(val);
    node->left = build_range(preorder, index_of, pos, lo, mid);
    node->right = build_range(preorder, index_of, pos, mid + 1, hi);
    return node;
}

TreeNode* build_tree(vector<int>& preorder, vector<int>& inorder) {
    unordered_map<int, int> index_of;
    for (int i = 0; i < (int)inorder.size(); i++) index_of[inorder[i]] = i;
    int pos = 0;
    return build_range(preorder, index_of, pos, 0, (int)inorder.size());
}
```

Each node is created once and each lookup is $O(1)$, so the time is $O(n)$, and the space is $O(n)$ for the dictionary plus $O(h)$ for the recursion. The same idea works for _postorder plus inorder_, where the root is the **last** value of the postorder (and one then builds the right subtree before the left).

## 8.3 Flattening into a chain

To **flatten** a tree means to rewire it in place into a chain that uses only right links, in preorder. For `[1, 2, 5, 3, 4, None, 6]` the chain is `1 -> 2 -> 3 -> 4 -> 5 -> 6`.

A pleasant way to see it: in the chain every node's right link must point to the node that comes **right after it in preorder**. If we visit the nodes in the exact reverse of preorder, then at each node the correct "next" is simply the node we handled just before. The reverse of preorder (node, left, right) is (right, left, node). So we recurse into the right child first, then the left child, and then we fix the current node: its `right` becomes the previously handled node `prev`, its `left` becomes `None`, and it becomes the new `prev`. This is exactly the problem _Flatten a Binary Tree_.

```python
def flatten(root):
    prev = None

    def go(node):
        nonlocal prev
        if node is None:
            return
        go(node.right)
        go(node.left)
        node.right = prev
        node.left = None
        prev = node

    go(root)
    return root


def build(values):
    if not values:
        return None
    root = TreeNode(values[0])
    line = [root]
    head = 0
    i = 1
    while head < len(line) and i < len(values):
        node = line[head]
        head += 1
        if values[i] is not None:
            node.left = TreeNode(values[i])
            line.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            line.append(node.right)
        i += 1
    return root


chain = flatten(build([1, 2, 5, 3, 4, None, 6]))
assert to_list(chain) == [1, None, 2, None, 3, None, 4, None, 5, None, 6]
assert flatten(None) is None
```

```cpp
const int NIL = INT_MIN;

TreeNode* build(const vector<int>& values) {
    if (values.empty()) return nullptr;
    TreeNode* root = new TreeNode(values[0]);
    vector<TreeNode*> line = {root};
    size_t head = 0, i = 1;
    while (head < line.size() && i < values.size()) {
        TreeNode* node = line[head++];
        if (values[i] != NIL) {
            node->left = new TreeNode(values[i]);
            line.push_back(node->left);
        }
        i++;
        if (i < values.size() && values[i] != NIL) {
            node->right = new TreeNode(values[i]);
            line.push_back(node->right);
        }
        i++;
    }
    return root;
}

void flatten_go(TreeNode* node, TreeNode*& prev) {
    if (node == nullptr) return;
    flatten_go(node->right, prev);
    flatten_go(node->left, prev);
    node->right = prev;
    node->left = nullptr;
    prev = node;
}

TreeNode* flatten(TreeNode* root) {
    TreeNode* prev = nullptr;
    flatten_go(root, prev);
    return root;
}
```

The time is $O(n)$ and the space is $O(h)$ for the recursion. If you want constant extra memory, there is a loop version. At a node with a left child, find the **rightmost node of the left subtree** (it is the last node of the left part in preorder), attach the old right subtree to it, move the whole left subtree over to the right, and clear the left link. Then step to the right and repeat.

```python
def flatten_in_place(root):
    cur = root
    while cur is not None:
        if cur.left is not None:
            tail = cur.left
            while tail.right is not None:
                tail = tail.right
            tail.right = cur.right        # old right part goes after the left part
            cur.right = cur.left          # left part moves to the right
            cur.left = None
        cur = cur.right
    return root


chain2 = flatten_in_place(build([1, 2, 5, 3, 4, None, 6]))
assert to_list(chain2) == [1, None, 2, None, 3, None, 4, None, 5, None, 6]
```

```cpp
TreeNode* flatten_in_place(TreeNode* root) {
    TreeNode* cur = root;
    while (cur != nullptr) {
        if (cur->left != nullptr) {
            TreeNode* tail = cur->left;
            while (tail->right != nullptr) tail = tail->right;
            tail->right = cur->right;
            cur->right = cur->left;
            cur->left = nullptr;
        }
        cur = cur->right;
    }
    return root;
}
```

Every link is walked a bounded number of times in total, so this is $O(n)$ time and $O(1)$ extra space.

## 8.4 Check yourself

1. Which traversal gives the root first, and what does the inorder list tell us about it?
2. Why must we build the left subtree before the right one when reading from the preorder?
3. Why do we make a dictionary of positions in the inorder list?
4. In the flatten code, why do we visit the right child before the left child?

# Chapter 9. Trees as maps of roads

## 9.1 The missing parent link

A `TreeNode` knows only its children, so from a node we can only walk **down**. But many questions treat the tree like a network of roads where you may walk to a neighbour in any direction: "how far is this node from the target?" or "if a fire starts here, how fast does it spread?" In such a question a node has up to three neighbours: its left child, its right child and its **parent**.

The fix is simple: do one walk through the whole tree first and store each node's parent in a dictionary (a **parent map**). We also store a dictionary from value to node, so that we can find the starting node from the number the problem gives. After that, a BFS like the one in Chapter 4 can spread out from any node in all three directions. One thing to remember: because we can now walk back up, we must keep a set of **seen** nodes so that we never step back to where we came from.

```python
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build(values):
    if not values:
        return None
    root = TreeNode(values[0])
    line = [root]
    head = 0
    i = 1
    while head < len(line) and i < len(values):
        node = line[head]
        head += 1
        if values[i] is not None:
            node.left = TreeNode(values[i])
            line.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            line.append(node.right)
        i += 1
    return root


def parent_map(root):
    parent = {root: None}
    by_value = {root.val: root}
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for child in (node.left, node.right):
            if child is not None:
                parent[child] = node
                by_value[child.val] = child
                queue.append(child)
    return parent, by_value


tree = build([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
parent, by_value = parent_map(tree)
assert parent[by_value[7]].val == 2
assert parent[tree] is None
```

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {}
};

const int NIL = INT_MIN;

TreeNode* build(const vector<int>& values) {
    if (values.empty()) return nullptr;
    TreeNode* root = new TreeNode(values[0]);
    vector<TreeNode*> line = {root};
    size_t head = 0, i = 1;
    while (head < line.size() && i < values.size()) {
        TreeNode* node = line[head++];
        if (values[i] != NIL) {
            node->left = new TreeNode(values[i]);
            line.push_back(node->left);
        }
        i++;
        if (i < values.size() && values[i] != NIL) {
            node->right = new TreeNode(values[i]);
            line.push_back(node->right);
        }
        i++;
    }
    return root;
}

pair<unordered_map<TreeNode*, TreeNode*>, unordered_map<int, TreeNode*>> parent_map(TreeNode* root) {
    unordered_map<TreeNode*, TreeNode*> parent;
    unordered_map<int, TreeNode*> by_value;
    parent[root] = nullptr;
    by_value[root->val] = root;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        TreeNode* node = q.front();
        q.pop();
        for (TreeNode* child : {node->left, node->right}) {
            if (child != nullptr) {
                parent[child] = node;
                by_value[child->val] = child;
                q.push(child);
            }
        }
    }
    return {parent, by_value};
}
```

This takes $O(n)$ time and $O(n)$ space. We assume the tree has at least one node, which holds for the problems below.

## 9.2 Nodes at distance K

Now find all nodes exactly `k` edges away from a target node. Starting at the target, we spread outwards one step at a time. After step 1 we hold all nodes at distance 1 (its parent and children), after step 2 all nodes at distance 2, and so on. After `k` steps, the nodes we hold are the answer. Each step looks at the three neighbours of every node we hold and keeps those not seen before.

On `[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]` with target `5`: distance 0 is `{5}`; distance 1 is `{3, 6, 2}`; distance 2 is `{1, 7, 4}`, which sorted is `[1, 4, 7]`. This is exactly the problem _Nodes at Distance K_.

```python
def distance_k(root, target, k):
    parent, by_value = parent_map(root)
    start = by_value[target]
    seen = {start}
    frontier = [start]
    for _ in range(k):
        next_frontier = []
        for node in frontier:
            for neighbour in (node.left, node.right, parent[node]):
                if neighbour is not None and neighbour not in seen:
                    seen.add(neighbour)
                    next_frontier.append(neighbour)
        frontier = next_frontier
    return sorted(node.val for node in frontier)


assert distance_k(tree, 5, 2) == [1, 4, 7]
assert distance_k(tree, 5, 0) == [5]
assert distance_k(tree, 5, 1) == [2, 3, 6]
assert distance_k(tree, 5, 9) == []
```

```cpp
vector<int> distance_k(TreeNode* root, int target, int k) {
    auto [parent, by_value] = parent_map(root);
    TreeNode* start = by_value[target];
    unordered_set<TreeNode*> seen = {start};
    vector<TreeNode*> frontier = {start};
    for (int step = 0; step < k; step++) {
        vector<TreeNode*> next_frontier;
        for (TreeNode* node : frontier) {
            for (TreeNode* neighbour : {node->left, node->right, parent[node]}) {
                if (neighbour != nullptr && !seen.count(neighbour)) {
                    seen.insert(neighbour);
                    next_frontier.push_back(neighbour);
                }
            }
        }
        frontier = next_frontier;
    }
    vector<int> result;
    for (TreeNode* node : frontier) result.push_back(node->val);
    sort(result.begin(), result.end());
    return result;
}
```

The time is $O(n)$ plus the final sort, and the space is $O(n)$.

## 9.3 Time to burn a tree

A fire starts at one node and every minute spreads to all neighbours (parent and both children). How many minutes until everything burns? This is the same spreading process; we just do not stop after `k` steps. Instead we count steps until there is nothing new left to burn. The number of minutes is the number of steps in which something new caught fire, which equals the distance from the start to the farthest node.

Our counter starts at -1, so the first round (the start node itself, burning at minute 0) brings it to 0. For a tree with only the start node the loop runs once and the answer is 0, as required. On `[1, 5, 3, None, 4, 10, 6, 9, 2]` with start `3`, the fire goes: minute 0 `{3}`, minute 1 `{1, 10, 6}`, minute 2 `{5}`, minute 3 `{4}`, minute 4 `{9, 2}`. The answer is 4. This is exactly the problem _Time to Burn a Tree_.

```python
def time_to_burn(root, start):
    parent, by_value = parent_map(root)
    first = by_value[start]
    seen = {first}
    frontier = [first]
    minutes = -1
    while frontier:
        minutes += 1
        next_frontier = []
        for node in frontier:
            for neighbour in (node.left, node.right, parent[node]):
                if neighbour is not None and neighbour not in seen:
                    seen.add(neighbour)
                    next_frontier.append(neighbour)
        frontier = next_frontier
    return minutes


fire = build([1, 5, 3, None, 4, 10, 6, 9, 2])
assert time_to_burn(fire, 3) == 4
assert time_to_burn(build([1]), 1) == 0
assert time_to_burn(build([1, 2]), 1) == 1
```

```cpp
int time_to_burn(TreeNode* root, int start) {
    auto [parent, by_value] = parent_map(root);
    TreeNode* first = by_value[start];
    unordered_set<TreeNode*> seen = {first};
    vector<TreeNode*> frontier = {first};
    int minutes = -1;
    while (!frontier.empty()) {
        minutes++;
        vector<TreeNode*> next_frontier;
        for (TreeNode* node : frontier) {
            for (TreeNode* neighbour : {node->left, node->right, parent[node]}) {
                if (neighbour != nullptr && !seen.count(neighbour)) {
                    seen.insert(neighbour);
                    next_frontier.push_back(neighbour);
                }
            }
        }
        frontier = next_frontier;
    }
    return minutes;
}
```

The time and space are both $O(n)$. This is a first taste of graph search: the tree is just a graph with no loops, and the same BFS works on any network.

## 9.4 Maximum width by numbering positions

The **width** of a level is the distance between its leftmost and rightmost nodes, counting the empty places between them as if the tree were complete (every node having two children). The widest level might not be the one with the most nodes.

To count the empty places we give every node a **position number** as if the tree were stored in a complete tree: the root is 0, and the node at position $i$ has its left child at $2i$ and its right child at $2i+1$. Then, on each level, the width is `last position - first position + 1`.

```
level 0:            0
level 1:        0       1
level 2:      0   1   2   3
```

On `[1, 3, 2, 5, 3, None, 9]` the last level has positions 0, 1 and 3 (the `9`), so its width is $3 - 0 + 1 = 4$.

A word of caution. In a very deep tree the numbers $2i$ and $2i+1$ double at every level and would overflow. The cure is to **subtract the first position of the level** before computing the children's numbers, so the numbers restart near 0 on every level. Then they are never larger than the width of the level, and we can store them in `long long` in C++ (Python integers never overflow). This is exactly the problem _Maximum Width of a Binary Tree_.

```python
def max_width(root):
    if root is None:
        return 0
    best = 0
    level = [(root, 0)]                       # (node, position)
    while level:
        first = level[0][1]
        last = level[-1][1]
        best = max(best, last - first + 1)
        next_level = []
        for node, position in level:
            base = position - first           # restart numbering near 0
            if node.left:
                next_level.append((node.left, 2 * base))
            if node.right:
                next_level.append((node.right, 2 * base + 1))
        level = next_level
    return best


assert max_width(build([1, 3, 2, 5, 3, None, 9])) == 4
assert max_width(build([1, 3, 2, 5])) == 2
assert max_width(build([1, 3, 2, 5, None, None, 9, 6, None, 7])) == 7
assert max_width(None) == 0
```

```cpp
int max_width(TreeNode* root) {
    if (root == nullptr) return 0;
    long long best = 0;
    vector<pair<TreeNode*, long long>> level = {{root, 0}};
    while (!level.empty()) {
        long long first = level.front().second;
        long long last = level.back().second;
        best = max(best, last - first + 1);
        vector<pair<TreeNode*, long long>> next_level;
        for (auto& [node, position] : level) {
            long long base = position - first;
            if (node->left) next_level.push_back({node->left, 2 * base});
            if (node->right) next_level.push_back({node->right, 2 * base + 1});
        }
        level = next_level;
    }
    return (int)best;
}
```

The time is $O(n)$ and the space is $O(w)$ for the widest level. The last example shows why counting empty places matters: the last level holds only two nodes, but they are 7 places apart.

## 9.5 Check yourself

1. Why do we store the parent of each node before spreading out from the target?
2. Why do we need a `seen` set when spreading in three directions?
3. How is the time-to-burn answer related to the distance from the start node?
4. How are the position numbers of the children of the node at position $i$ computed, and why do we subtract the first position of the level?
