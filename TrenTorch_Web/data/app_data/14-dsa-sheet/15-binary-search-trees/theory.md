> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Binary search trees)

This page teaches binary search trees, or BSTs, from the single rule that defines them to a few of the harder interview questions. It assumes you know what a binary tree is (a node with a left child and a right child) and how a recursive function walks one. If those words feel new, read the page on binary trees first. You will learn how to search, insert and delete in a BST, how to check that a tree really is a BST, why walking it in order gives sorted values, how to take it apart one value at a time, how to build balanced ones, and how to repair or measure a broken one.

The page is a staircase. **Chapter 1 is deliberately gentle**: one rule, one picture, and the simplest search. Each chapter after it adds one family of questions and uses only what came before. By the last chapter you will be ready for the hardest questions in this step. Every code example is shown in Python and in C++, so use whichever language you like.

# Chapter 1. The BST rule and searching

## 1.1 A tree with an ordering rule

In an ordinary binary tree the values can sit anywhere, so to find a value you must look at every node. A **binary search tree** adds one rule that makes searching fast. For every node:

all the values in its **left subtree** are smaller than the node's value, and all the values in its **right subtree** are larger.

Here is an example.

```
          8
        /   \
       3     10
      / \      \
     1   6      14
        / \     /
       4   7   13
```

Look at `8`: everything on its left (`3, 1, 6, 4, 7`) is smaller than 8, and everything on its right (`10, 14, 13`) is larger. Look at `3`: on its left is `1` (smaller), on its right are `6, 4, 7` (all larger than 3). The same holds for every node. In this page we assume all values in a BST are different (the problem statements say so too).

## 1.2 The rule covers whole subtrees

A very common mistake is to think that a node only has to be larger than its left child and smaller than its right child. That is not enough. Look at this tree.

```
      5
     / \
    1   8
       / \
      3   9
```

Every node is fine compared with its own two children (8 is bigger than 3 and smaller than 9). But `3` sits in the **right subtree of 5**, and 3 is smaller than 5. So this is **not** a BST. The rule is about _everything_ below a node, not just the direct children. We will return to this trap in the chapter about validating BSTs.

## 1.3 Searching by comparing

The rule makes searching easy. To look for a value `x`, start at the root and compare. If `x` equals the node's value, we found it. If `x` is smaller, then by the rule it can only be in the left subtree, so the whole right subtree can be ignored. If `x` is larger, it can only be in the right subtree. So at each step we throw away one half of the remaining tree, just like binary search on a sorted list. We stop when we find the value or fall off the tree (reach `None`).

In the problem _Search in a BST_ we return the **subtree** whose root holds the value (the node together with everything below it), or an empty tree when the value is missing. Since a node already is the root of its subtree, we simply return the node we stop at. This is exactly the problem _Search in a BST_.

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


def search_bst(root, val):
    node = root
    while node is not None and node.val != val:
        node = node.left if val < node.val else node.right
    return node


tree = build([4, 2, 7, 1, 3])
assert to_list(search_bst(tree, 2)) == [2, 1, 3]
assert search_bst(tree, 7).val == 7
assert search_bst(tree, 5) is None
```

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {}
};

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

TreeNode* search_bst(TreeNode* root, int val) {
    TreeNode* node = root;
    while (node != nullptr && node->val != val) {
        node = (val < node->val) ? node->left : node->right;
    }
    return node;
}
```

(The helpers `TreeNode`, `build` and `to_list` turn a level-order list like `[4, 2, 7, 1, 3]` into nodes and back. We repeat them at the start of each chapter so that every chapter stands on its own, and will not explain them again.)

The loop makes one step down per round, so the time is $O(h)$ where $h$ is the height of the tree, and the extra space is $O(1)$.

## 1.4 Inorder gives sorted values

Here is the most useful fact about BSTs. Remember **inorder** traversal: visit the left subtree, then the node, then the right subtree. In a BST everything on the left is smaller than the node and everything on the right is larger, and this is true at every level. So inorder visits the values in **increasing order**.

On our first tree the inorder walk gives `1, 3, 4, 6, 7, 8, 10, 13, 14`, which is sorted. The reverse also holds, in a useful way: if an inorder walk is _not_ increasing, the tree is not a BST. A lot of BST problems become easy when you think "this is really a question about a sorted list".

```python
def inorder_values(root):
    out = []

    def visit(node):
        if node is None:
            return
        visit(node.left)
        out.append(node.val)
        visit(node.right)

    visit(root)
    return out


big = build([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13])
assert inorder_values(big) == [1, 3, 4, 6, 7, 8, 10, 13, 14]
assert inorder_values(build([5, 1, 8, None, None, 3, 9])) == [1, 5, 3, 8, 9]
```

```cpp
void visit_inorder(TreeNode* node, vector<int>& out) {
    if (node == nullptr) return;
    visit_inorder(node->left, out);
    out.push_back(node->val);
    visit_inorder(node->right, out);
}

vector<int> inorder_values(TreeNode* root) {
    vector<int> out;
    visit_inorder(root, out);
    return out;
}
```

The second assert shows the bad tree from section 1.2: its inorder list `1, 5, 3, 8, 9` goes down from 5 to 3, which exposes the problem.

## 1.5 Why height matters

Every BST operation in this chapter costs one step per level, so it costs $O(h)$. If the tree is well balanced (both sides roughly equally deep) then $h$ is about $\log_2 n$, and a tree of a million nodes needs only about 20 steps. But if you insert the values `1, 2, 3, 4, ...` in order, each new value goes to the right of the last one and the tree becomes a long chain with $h = n$. Then searching is as slow as scanning a list. That is why we also care about _balanced_ trees, which the later chapters build.

## 1.6 Check yourself

1. State the BST rule in one sentence.
2. Why is "each node is larger than its left child and smaller than its right child" not enough?
3. What does an inorder walk of a BST produce?
4. When is a search in a BST as slow as a search in a list?

# Chapter 2. Insert and delete

## 2.1 Inserting a new leaf

To add a value to a BST we first search for it. Since it is not in the tree yet, the search falls off the tree at some empty place, and that empty place is exactly where the new value belongs. We attach a new node there. No other node moves.

The recursive version reads very naturally. If the tree is empty, the new node is the whole tree. Otherwise, if the value is smaller than the current node, the new node belongs in the left subtree, so we replace the left subtree by "the left subtree with the value inserted". Do the same on the right for a larger value. At the end we return the root of the tree we were given. This is exactly the problem _Insert into a BST_.

For `[4, 2, 7, 1, 3]` and `5`: 5 is larger than 4, go right to `7`; 5 is smaller than 7, go left, which is empty. So `5` becomes the left child of `7`.

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


def insert_into_bst(root, val):
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)
    return root


assert to_list(insert_into_bst(build([4, 2, 7, 1, 3]), 5)) == [4, 2, 7, 1, 3, 5]
assert to_list(insert_into_bst(None, 9)) == [9]
assert to_list(insert_into_bst(build([4, 2, 7, 1, 3]), 0)) == [4, 2, 7, 1, 3, None, None, 0]
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

TreeNode* insert_into_bst(TreeNode* root, int val) {
    if (root == nullptr) return new TreeNode(val);
    if (val < root->val) {
        root->left = insert_into_bst(root->left, val);
    } else {
        root->right = insert_into_bst(root->right, val);
    }
    return root;
}
```

The time is $O(h)$ and the space is $O(h)$ for the recursion.

## 2.2 Deleting a node

Deleting is the first BST operation with some care needed, because removing a node must keep the rule true for everything else. First we find the node by searching, as before. When we find it, there are three cases.

If the node is a **leaf**, we simply remove it. If it has **one child**, we replace the node by that child: the child's whole subtree takes the place of the deleted node, and all the ordering is still correct, since everything in it was already on the right side of the deleted node's ancestors.

If it has **two children**, we cannot just remove it, because there are two subtrees and only one place. Instead we replace its value with another value that keeps the rule true: its **inorder successor**, which is the next larger value in the tree, found as the smallest value in the right subtree (go to the right child, then keep going left). The successor is larger than everything on the left and smaller than everything else on the right, so it can sit at the root of the two subtrees. After copying its value up, we delete the successor from the right subtree. The successor has no left child (we stopped going left), so that deletion is one of the easy cases.

For `[5, 3, 6, 2, 4, None, 7]` and `key = 3`: the node `3` has two children, `2` and `4`. The smallest value in its right subtree is `4`, so `3` becomes `4`, and the old `4` leaf is deleted. This is exactly the problem _Delete a Node from a BST_.

```python
def delete_node(root, key):
    if root is None:
        return None
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:            # zero children, or only a right child
            return root.right
        if root.right is None:           # only a left child
            return root.left
        successor = root.right           # two children: smallest value on the right
        while successor.left is not None:
            successor = successor.left
        root.val = successor.val
        root.right = delete_node(root.right, successor.val)
    return root


start = [5, 3, 6, 2, 4, None, 7]
assert to_list(delete_node(build(start), 3)) == [5, 4, 6, 2, None, None, 7]
assert to_list(delete_node(build(start), 5)) == [6, 3, 7, 2, 4]
assert to_list(delete_node(build(start), 7)) == [5, 3, 6, 2, 4]
assert to_list(delete_node(build(start), 99)) == start
assert delete_node(None, 1) is None
```

```cpp
TreeNode* delete_node(TreeNode* root, int key) {
    if (root == nullptr) return nullptr;
    if (key < root->val) {
        root->left = delete_node(root->left, key);
    } else if (key > root->val) {
        root->right = delete_node(root->right, key);
    } else {
        if (root->left == nullptr) return root->right;
        if (root->right == nullptr) return root->left;
        TreeNode* successor = root->right;
        while (successor->left != nullptr) successor = successor->left;
        root->val = successor->val;
        root->right = delete_node(root->right, successor->val);
    }
    return root;
}
```

The time is $O(h)$: one walk down to the node and at most one more walk down to its successor. The space is $O(h)$ for the recursion.

## 2.3 Check yourself

1. Where does a new value end up when it is inserted into a BST?
2. What are the three cases when deleting a node?
3. Why is the smallest value of the right subtree a safe replacement for a node with two children?
4. What does a node's inorder successor look like in terms of its left child?

# Chapter 3. Walking down with comparisons

## 3.1 One comparison per step

Searching worked because at each node a single comparison tells us which half of the tree to keep. Many questions about a BST have the same character. We walk down from the root, make one comparison at each node, and remember a small piece of information about the nodes we pass. The answer is ready when we fall off the tree. Every question in this chapter costs $O(h)$ steps (or a pruned walk of the tree) and uses little memory.

## 3.2 Range sum with pruning

Find the sum of all values that lie between `low` and `high`, both included. We could add up every node in the tree, but the BST rule lets us skip big parts. If the current value is **below** `low`, then it and everything in its left subtree are too small, so we only continue to the right. If it is **above** `high`, then it and its right subtree are too large, so we only continue to the left. Otherwise the value is in the range: count it and look at both sides. Skipping parts of the tree like this is called **pruning**.

For `[10, 5, 15, 3, 7, None, 18]` with `low = 7` and `high = 15` we count 10, 7 and 15, for a total of 32, and never look at `3` or `18` at all. This is exactly the problem _Range Sum of a BST_.

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


def range_sum(root, low, high):
    if root is None:
        return 0
    if root.val < low:
        return range_sum(root.right, low, high)
    if root.val > high:
        return range_sum(root.left, low, high)
    return root.val + range_sum(root.left, low, high) + range_sum(root.right, low, high)


assert range_sum(build([10, 5, 15, 3, 7, None, 18]), 7, 15) == 32
assert range_sum(build([10, 5, 15, 3, 7, None, 18]), 20, 30) == 0
assert range_sum(None, 1, 5) == 0
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

int range_sum(TreeNode* root, int low, int high) {
    if (root == nullptr) return 0;
    if (root->val < low) return range_sum(root->right, low, high);
    if (root->val > high) return range_sum(root->left, low, high);
    return root->val + range_sum(root->left, low, high) + range_sum(root->right, low, high);
}
```

In the worst case every node is in the range, so the time is $O(n)$; with a small range it is closer to $O(h + k)$ where $k$ is the number of values counted. The space is $O(h)$.

## 3.3 Floor and ceil

For a number `x`, the **floor** is the largest value in the tree that is at most `x`, and the **ceil** is the smallest value that is at least `x`. They are the neighbours of `x` in the sorted order of the tree. We walk down comparing with `x` and remember the best candidate seen so far.

If the node's value equals `x`, floor and ceil are both `x`. If the node's value is **less** than `x`, it is a candidate for the floor (it is at most `x`), and a better floor could only be larger, so it must be in the right subtree: remember it and go right. If the node's value is **greater** than `x`, it is a candidate for the ceil, and a better ceil must be smaller, so remember it and go left. If nothing was remembered, the answer is `-1`.

For `[8, 4, 12, 2, 6, 10, 14]` and `x = 5`: at `8`, ceil is 8, go left; at `4`, floor is 4, go right; at `6`, ceil is 6, go left, which is empty. The answer is `[4, 6]`. This is exactly the problem _Floor and Ceil in a BST_.

```python
def floor_ceil(root, x):
    floor, ceil = -1, -1
    node = root
    while node is not None:
        if node.val == x:
            return [x, x]
        if node.val < x:
            floor = node.val
            node = node.right
        else:
            ceil = node.val
            node = node.left
    return [floor, ceil]


sample = build([8, 4, 12, 2, 6, 10, 14])
assert floor_ceil(sample, 5) == [4, 6]
assert floor_ceil(sample, 1) == [-1, 2]
assert floor_ceil(sample, 15) == [14, -1]
assert floor_ceil(sample, 10) == [10, 10]
```

```cpp
vector<int> floor_ceil(TreeNode* root, int x) {
    int floor_value = -1, ceil_value = -1;
    TreeNode* node = root;
    while (node != nullptr) {
        if (node->val == x) return {x, x};
        if (node->val < x) {
            floor_value = node->val;
            node = node->right;
        } else {
            ceil_value = node->val;
            node = node->left;
        }
    }
    return {floor_value, ceil_value};
}
```

The time is $O(h)$ and the space is $O(1)$.

## 3.4 Closest value to a target

To find the value closest to a `target` (which can be any number), notice that the closest value is either the floor or the ceil of the target. So we can use the same walk: at each node, compare its distance to the target with the best distance so far and keep the better one; if the two distances are equal, keep the smaller value. Then go left if the target is smaller than the node and right otherwise, because only that side can still contain a closer value.

For `[4, 2, 5, 1, 3]` and target `6`: we visit 4 (distance 2), then 5 (distance 1), and fall off the tree; the answer is 5. For target `3.5` the values 3 and 4 are equally close, so the smaller one, 3, is returned. This is exactly the problem _Closest Value in a BST_.

```python
def closest_value(root, target):
    best = root.val
    node = root
    while node is not None:
        gap = abs(node.val - target)
        best_gap = abs(best - target)
        if gap < best_gap or (gap == best_gap and node.val < best):
            best = node.val
        node = node.left if target < node.val else node.right
    return best


close = build([4, 2, 5, 1, 3])
assert closest_value(close, 3) == 3
assert closest_value(close, 6) == 5
assert closest_value(close, 3.5) == 3
assert closest_value(close, -10) == 1
```

```cpp
int closest_value(TreeNode* root, double target) {
    int best = root->val;
    TreeNode* node = root;
    while (node != nullptr) {
        double gap = fabs(node->val - target);
        double best_gap = fabs(best - target);
        if (gap < best_gap || (gap == best_gap && node->val < best)) {
            best = node->val;
        }
        node = (target < node->val) ? node->left : node->right;
    }
    return best;
}
```

The time is $O(h)$ and the space is $O(1)$.

## 3.5 Inorder successor

The **inorder successor** of a value `p` is the next larger value in the tree, which is the node that comes right after `p` in the sorted order. If `p` has a right subtree, it is the smallest value of that subtree. In general we can find it with a walk from the root: if `p` is smaller than the current node, the current node is a candidate (it is larger than `p`), so remember it and go left to look for a closer, smaller candidate. If `p` is larger than or equal to the current node, the successor is somewhere to the right, so go right without remembering. The last remembered node is the answer, or `None` if we never remembered one.

For `[2, 1, 3]` and `p = 1` we remember `2`, go left, find `1`, go right (empty), and answer `2`. For `p = 3` nothing is ever remembered and the answer is `None`. This is exactly the problem _Inorder Successor_.

```python
def inorder_successor(root, p):
    successor = None
    node = root
    while node is not None:
        if p < node.val:
            successor = node
            node = node.left
        else:
            node = node.right
    return successor


small = build([2, 1, 3])
assert inorder_successor(small, 1).val == 2
assert inorder_successor(small, 3) is None
deeper = build([5, 3, 6, 2, 4, None, None, 1])
assert inorder_successor(deeper, 4).val == 5
assert inorder_successor(deeper, 3).val == 4
```

```cpp
TreeNode* inorder_successor(TreeNode* root, int p) {
    TreeNode* successor = nullptr;
    TreeNode* node = root;
    while (node != nullptr) {
        if (p < node->val) {
            successor = node;
            node = node->left;
        } else {
            node = node->right;
        }
    }
    return successor;
}
```

The time is $O(h)$ and the space is $O(1)$.

## 3.6 Lowest common ancestor in a BST

The **lowest common ancestor** of two values is the lowest node that has both of them in its subtree (a node counts as being in its own subtree). In a general tree we had to search both sides. In a BST the ordering gives a shortcut: stand at the root. If both values are smaller than the node, they are both in the left subtree, so the answer is there; go left. If both are larger, go right. In every other case, one value is on each side (or one of them is the node itself), so this node is the point where their paths split and it is the answer.

For `[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]`: for the values 2 and 8, we split at the root, so the answer is `6`. For 2 and 4, both are smaller than 6 so we go to `2`, where 2 equals the node and 4 is larger, so the answer is `2`. This is exactly the problem _Lowest Common Ancestor in a BST_.

```python
def lca_bst(root, p, q):
    node = root
    while node is not None:
        if p < node.val and q < node.val:
            node = node.left
        elif p > node.val and q > node.val:
            node = node.right
        else:
            return node
    return None


lca_tree = build([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
assert lca_bst(lca_tree, 2, 8).val == 6
assert lca_bst(lca_tree, 2, 4).val == 2
assert lca_bst(lca_tree, 3, 5).val == 4
assert lca_bst(lca_tree, 7, 9).val == 8
```

```cpp
TreeNode* lca_bst(TreeNode* root, int p, int q) {
    TreeNode* node = root;
    while (node != nullptr) {
        if (p < node->val && q < node->val) {
            node = node->left;
        } else if (p > node->val && q > node->val) {
            node = node->right;
        } else {
            return node;
        }
    }
    return nullptr;
}
```

The time is $O(h)$ and the space is $O(1)$, better than the $O(n)$ time of the general-tree version.

## 3.7 Check yourself

1. In the range sum, which side can we skip when the node's value is below `low`?
2. Why does a node smaller than `x` become a floor candidate and send us to the right?
3. When does the BST version of the lowest common ancestor stop going down?
4. What is the cost of all the walks in this chapter in terms of the height $h$?

# Chapter 4. Checking that a tree is a BST

## 4.1 The trap of checking only children

How do we test that a tree really is a BST? The obvious idea is to check, at every node, that the left child is smaller and the right child is larger. Section 1.2 already showed why this fails: a node deep in the tree must also respect the nodes far above it. In the tree `[5, 1, 8, None, None, 3, 9]` every node agrees with its own children, but `3` sits in the right subtree of `5` while being smaller than 5.

## 4.2 Validating with ranges

A better way is to give each node the **range of values it is allowed to have**. The root may hold anything, so its range is from minus infinity to plus infinity. When we go to the left child, every value there must be smaller than the current node, so the upper limit of the range becomes the node's value. When we go to the right child, the lower limit becomes the node's value. A node is fine if its value is strictly inside its range, and the tree is a BST when every node is fine.

You can picture the range shrinking as we walk down, a little like the search interval in binary search. On the bad tree above: the root `5` has range $(-\infty, \infty)$; its right child `8` has range $(5, \infty)$ and is fine; the left child of `8`, which is `3`, gets the range $(5, 8)$, and 3 is outside it, so the tree is not a BST.

We use _strictly_ smaller and larger because the values of a BST are all different. This is exactly the problem _Validate a BST_.

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


def is_valid_bst(root):
    def ok(node, low, high):              # every value here must be in (low, high)
        if node is None:
            return True
        if node.val <= low or node.val >= high:
            return False
        return ok(node.left, low, node.val) and ok(node.right, node.val, high)

    return ok(root, float("-inf"), float("inf"))


assert is_valid_bst(build([2, 1, 3]))
assert not is_valid_bst(build([5, 1, 4, None, None, 3, 6]))
assert not is_valid_bst(build([5, 1, 8, None, None, 3, 9]))
assert not is_valid_bst(build([2, 2, 2]))
assert is_valid_bst(None)
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

bool valid_in_range(TreeNode* node, long long low, long long high) {
    if (node == nullptr) return true;
    if (node->val <= low || node->val >= high) return false;
    return valid_in_range(node->left, low, node->val) && valid_in_range(node->right, node->val, high);
}

bool is_valid_bst(TreeNode* root) {
    return valid_in_range(root, LLONG_MIN, LLONG_MAX);
}
```

We use `long long` for the limits in C++ so that a node holding the smallest or largest `int` is still handled correctly. Each node is visited once, so the time is $O(n)$ and the space is $O(h)$.

## 4.3 Validating with inorder

The second way uses Section 1.4: a tree is a BST exactly when its inorder values are strictly increasing. We do not need to store the whole list; we only keep the previous value and compare. We walk the tree in order with a stack (go left, pop, go right), and every time we pop a node we check that it is larger than the previous one.

```python
def is_valid_bst_inorder(root):
    stack = []
    node = root
    previous = None
    while node is not None or stack:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if previous is not None and node.val <= previous:
            return False
        previous = node.val
        node = node.right
    return True


assert is_valid_bst_inorder(build([2, 1, 3]))
assert not is_valid_bst_inorder(build([5, 1, 4, None, None, 3, 6]))
assert not is_valid_bst_inorder(build([2, 2, 2]))
```

```cpp
bool is_valid_bst_inorder(TreeNode* root) {
    vector<TreeNode*> stack;
    TreeNode* node = root;
    bool has_previous = false;
    int previous = 0;
    while (node != nullptr || !stack.empty()) {
        while (node != nullptr) {
            stack.push_back(node);
            node = node->left;
        }
        node = stack.back();
        stack.pop_back();
        if (has_previous && node->val <= previous) return false;
        previous = node->val;
        has_previous = true;
        node = node->right;
    }
    return true;
}
```

Both versions run in $O(n)$ time and $O(h)$ space. Pick whichever you find easier to write; the range version also generalises nicely to other questions (see the last chapter).

## 4.4 Check yourself

1. Why is it not enough to compare each node with its two children?
2. How do the limits of the allowed range change when we step to the left child, and to the right child?
3. What must be true about the inorder values of a BST?
4. Why do we use `<=` and `>=` in the failing tests?

# Chapter 5. Inorder is a sorted list

## 5.1 Turning questions into sorted-list questions

Because inorder gives the values in increasing order, a BST behaves like a sorted list that we can read one value at a time. So whenever a question is about ranks ("the third smallest"), neighbours ("the closest pair") or running totals ("the sum of everything larger"), we can think about a sorted list and then do the same thing during an inorder walk, with no need to build the list at all. The tools are the stack-based inorder walk (go left, pop, go right) and its mirror image (go right, pop, go left), which reads the values from the largest to the smallest.

## 5.2 Kth smallest by early stop

The **k-th smallest** value is the k-th value that the inorder walk produces. So we walk in order, count the values as they are popped, and stop as soon as the count reaches `k`. We do not need to visit the rest of the tree.

For `[5, 3, 6, 2, 4, None, None, 1]` and `k = 3`: the inorder values are `1, 2, 3, 4, 5, 6`, and the third one is `3`. This is exactly the problem _Kth Smallest in a BST_.

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


def kth_smallest(root, k):
    stack = []
    node = root
    while node is not None or stack:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right
    return -1                              # k is larger than the number of nodes


assert kth_smallest(build([3, 1, 4, None, 2]), 1) == 1
assert kth_smallest(build([5, 3, 6, 2, 4, None, None, 1]), 3) == 3
assert kth_smallest(build([5, 3, 6, 2, 4, None, None, 1]), 6) == 6
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

int kth_smallest(TreeNode* root, int k) {
    vector<TreeNode*> stack;
    TreeNode* node = root;
    while (node != nullptr || !stack.empty()) {
        while (node != nullptr) {
            stack.push_back(node);
            node = node->left;
        }
        node = stack.back();
        stack.pop_back();
        k--;
        if (k == 0) return node->val;
        node = node->right;
    }
    return -1;
}
```

The walk pops at most $k$ nodes and pushes the left path to the smallest value first, so the time is $O(h + k)$ and the space is $O(h)$.

## 5.3 Smallest gap between values

What is the smallest absolute difference between any two values in the BST? In a sorted list, the two closest values are always **neighbours**: if two values had another one between them, that other value would be closer to both. So we only need to compare each value in the inorder walk with the one just before it, and keep the smallest difference. We carry the previous node along the walk.

For `[4, 2, 6, 1, 3]` the inorder values are `1, 2, 3, 4, 6`, and the gaps are 1, 1, 1, 2. The smallest is 1. This is exactly the problem _Minimum Difference in a BST_.

```python
def min_diff(root):
    best = float("inf")
    previous = None

    def visit(node):
        nonlocal best, previous
        if node is None:
            return
        visit(node.left)
        if previous is not None:
            best = min(best, node.val - previous)
        previous = node.val
        visit(node.right)

    visit(root)
    return best


assert min_diff(build([4, 2, 6, 1, 3])) == 1
assert min_diff(build([1, 0, 48, None, None, 12, 49])) == 1
assert min_diff(build([10, 3, 20])) == 7
```

```cpp
void min_diff_visit(TreeNode* node, bool& has_previous, int& previous, int& best) {
    if (node == nullptr) return;
    min_diff_visit(node->left, has_previous, previous, best);
    if (has_previous) best = min(best, node->val - previous);
    previous = node->val;
    has_previous = true;
    min_diff_visit(node->right, has_previous, previous, best);
}

int min_diff(TreeNode* root) {
    int best = INT_MAX;
    bool has_previous = false;
    int previous = 0;
    min_diff_visit(root, has_previous, previous, best);
    return best;
}
```

The time is $O(n)$ and the space is $O(h)$.

## 5.4 Greater sum tree by reverse inorder

Now every node's value must become its **own value plus the sum of all values larger than it**. In a sorted list this is a running total from the largest value down to the smallest. So we walk the tree in the **reverse** inorder: right subtree first, then the node, then the left subtree. That visits the values from the largest to the smallest. We keep a running `total`; at each node we add its value to the total and then store the total in the node.

For `[2, 1, 3]` the values are visited as 3, 2, 1: the totals become 3, then 5, then 6, so the tree becomes `[5, 6, 3]`. This is exactly the problem _BST to Greater Sum Tree_.

```python
def greater_tree(root):
    total = 0

    def visit(node):
        nonlocal total
        if node is None:
            return
        visit(node.right)
        total += node.val
        node.val = total
        visit(node.left)

    visit(root)
    return root


assert to_list(greater_tree(build([2, 1, 3]))) == [5, 6, 3]
assert to_list(greater_tree(build([0, None, 1]))) == [1, None, 1]
big = build([4, 1, 6, 0, 2, 5, 7, None, None, None, 3, None, None, None, 8])
assert to_list(greater_tree(big)) == [30, 36, 21, 36, 35, 26, 15, None, None, None, 33, None, None, None, 8]
```

```cpp
void greater_visit(TreeNode* node, int& total) {
    if (node == nullptr) return;
    greater_visit(node->right, total);
    total += node->val;
    node->val = total;
    greater_visit(node->left, total);
}

TreeNode* greater_tree(TreeNode* root) {
    int total = 0;
    greater_visit(root, total);
    return root;
}
```

The time is $O(n)$ and the space is $O(h)$.

## 5.5 Merging two BSTs into a sorted list

Given two BSTs, return all their values in one sorted list. Each tree gives its values in sorted order through an inorder walk, so the question is just to **merge two sorted lists**, which we do with two pointers: look at the smallest unused value of each list, take the smaller one, and move that pointer forward. When one list runs out, add the rest of the other.

For `[2, 1, 4]` and `[1, 0, 3]` the lists are `1, 2, 4` and `0, 1, 3`, and merging gives `0, 1, 1, 2, 3, 4`. This is exactly the problem _Merge Two BSTs into a Sorted List_.

```python
def inorder_values(root):
    out = []

    def visit(node):
        if node is None:
            return
        visit(node.left)
        out.append(node.val)
        visit(node.right)

    visit(root)
    return out


def merge_two_bsts(root1, root2):
    a = inorder_values(root1)
    b = inorder_values(root2)
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


assert merge_two_bsts(build([2, 1, 4]), build([1, 0, 3])) == [0, 1, 1, 2, 3, 4]
assert merge_two_bsts(None, build([5])) == [5]
assert merge_two_bsts(None, None) == []
```

```cpp
void collect_inorder(TreeNode* node, vector<int>& out) {
    if (node == nullptr) return;
    collect_inorder(node->left, out);
    out.push_back(node->val);
    collect_inorder(node->right, out);
}

vector<int> inorder_values(TreeNode* root) {
    vector<int> out;
    collect_inorder(root, out);
    return out;
}

vector<int> merge_two_bsts(TreeNode* root1, TreeNode* root2) {
    vector<int> a = inorder_values(root1);
    vector<int> b = inorder_values(root2);
    vector<int> out;
    size_t i = 0, j = 0;
    while (i < a.size() && j < b.size()) {
        if (a[i] <= b[j]) {
            out.push_back(a[i++]);
        } else {
            out.push_back(b[j++]);
        }
    }
    while (i < a.size()) out.push_back(a[i++]);
    while (j < b.size()) out.push_back(b[j++]);
    return out;
}
```

If the trees have $m$ and $n$ nodes, the time is $O(m + n)$ and the space is $O(m + n)$. The next chapter shows how to avoid building the two lists by walking both trees step by step.

## 5.6 Check yourself

1. Why does kth smallest not need to visit the whole tree?
2. Why do we only compare each value with its inorder neighbour when looking for the smallest gap?
3. In which order must we walk the tree to build the greater sum tree, and why?
4. What classical list algorithm is used to merge the two inorder lists?

# Chapter 6. Iterators and two sum

## 6.1 An inorder walk you can pause

The stack-based inorder walk has a nice property: the stack remembers exactly where we are. If we stop after producing a value, the stack still holds the rest of the work, and we can continue later. We can wrap this into a small object called an **iterator**, which has two actions: `next()` gives the next larger value, and `has_next()` says whether there is one.

The stack always holds the nodes on a left-going path whose values are still to be produced. To produce the next value we pop the top node (the smallest remaining one), then push the left path of its right child, since that subtree holds the values that come next. The memory is only $O(h)$, the height, which is much less than $O(n)$ for a balanced tree, and each `next()` takes $O(1)$ time on average (every node is pushed and popped exactly once overall).

We can also make a **backward** iterator: swap the roles of left and right, and the values come out from the largest to the smallest.

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


class BSTIterator:
    def __init__(self, root, backward=False):
        self.stack = []
        self.backward = backward
        self._push_path(root)

    def _push_path(self, node):
        while node is not None:
            self.stack.append(node)
            node = node.right if self.backward else node.left

    def has_next(self):
        return len(self.stack) > 0

    def next(self):
        node = self.stack.pop()
        self._push_path(node.left if self.backward else node.right)
        return node.val


it = BSTIterator(build([7, 3, 15, None, None, 9, 20]))
order = []
while it.has_next():
    order.append(it.next())
assert order == [3, 7, 9, 15, 20]

back = BSTIterator(build([7, 3, 15, None, None, 9, 20]), True)
order = []
while back.has_next():
    order.append(back.next())
assert order == [20, 15, 9, 7, 3]
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

class BSTIterator {
    vector<TreeNode*> stack;
    bool backward;

    void push_path(TreeNode* node) {
        while (node != nullptr) {
            stack.push_back(node);
            node = backward ? node->right : node->left;
        }
    }

public:
    BSTIterator(TreeNode* root, bool back = false) : backward(back) {
        push_path(root);
    }

    bool has_next() { return !stack.empty(); }

    int next() {
        TreeNode* node = stack.back();
        stack.pop_back();
        push_path(backward ? node->left : node->right);
        return node->val;
    }
};
```

## 6.2 Two sum with two iterators

Are there two different nodes whose values add up to `k`? If the values were in a sorted list, we would use the classic **two-pointer** method: one pointer `lo` at the smallest value, one pointer `hi` at the largest. If `lo + hi` equals `k`, we are done. If the sum is too small, the only way to increase it is to move `lo` to the next larger value. If it is too large, move `hi` to the next smaller value. Stop when the pointers meet.

A BST gives us both walkers for free: the forward iterator plays the part of `lo`, and the backward iterator plays the part of `hi`. We never build the sorted list, so the memory is only $O(h)$. The loop condition `lo < hi` makes sure the two values come from different nodes, and also guarantees that the next call to either iterator has something to return.

For `[5, 3, 6, 2, 4, None, 7]` and `k = 9`: we start with `lo = 2` and `hi = 7`, and their sum is already 9, so the answer is `True` (the pair `3 + 6` works too). For `k = 28` the sum is always too small, so `lo` keeps moving up until it meets `hi`, and the answer is `False`. This is exactly the problem _Two Sum in a BST_.

```python
def find_target(root, k):
    if root is None:
        return False
    small = BSTIterator(root)
    large = BSTIterator(root, True)
    lo = small.next()
    hi = large.next()
    while lo < hi:
        total = lo + hi
        if total == k:
            return True
        if total < k:
            lo = small.next()
        else:
            hi = large.next()
    return False


pair_tree = build([5, 3, 6, 2, 4, None, 7])
assert find_target(pair_tree, 9)
assert find_target(pair_tree, 11)
assert not find_target(pair_tree, 28)
assert not find_target(build([2]), 4)
assert not find_target(None, 0)
```

```cpp
bool find_target(TreeNode* root, int k) {
    if (root == nullptr) return false;
    BSTIterator small(root, false);
    BSTIterator large(root, true);
    long long lo = small.next();
    long long hi = large.next();
    while (lo < hi) {
        long long total = lo + hi;
        if (total == k) return true;
        if (total < k) {
            lo = small.next();
        } else {
            hi = large.next();
        }
    }
    return false;
}
```

Each iterator moves over each node at most once, so the time is $O(n)$ and the space is $O(h)$. A different solution stores every value in a hash set and checks for `k - value`; it is just as fast in time but uses $O(n)$ memory and ignores the BST property.

## 6.3 Check yourself

1. What does the stack of the iterator contain at any moment?
2. After popping a node in `next()`, why do we push the left path of its right child?
3. How do we change the iterator to produce the values from largest to smallest?
4. In two sum, what happens to the pointers when the sum is too small, and when it is too large?

# Chapter 7. Building, balancing and trimming

## 7.1 Building a balanced BST from a sorted list

Suppose we have a sorted list and want to make a BST from it. If we insert the values one by one in order, we get a long chain (Chapter 1) and the height is $n$. A much better idea is to choose the **middle** value as the root: half of the values are smaller and go to its left, half are larger and go to its right. Then do the same for each half. The result is a **height-balanced** tree, one where at every node the heights of the two sides differ by at most 1.

The recursion works on a range of the list `[lo, hi]`. If the range is empty, return `None`. Otherwise take the middle index `(lo + hi) // 2` (for an even count this is the lower middle), make a node with that value, build its left subtree from `[lo, mid - 1]` and its right subtree from `[mid + 1, hi]`. For `[-10, -3, 0, 5, 9]` the middle is `0`; the left half `[-10, -3]` gives `-10` as the root with `-3` on its right; the right half `[5, 9]` gives `5` with `9` on its right. This is exactly the problem _Sorted Array to a Balanced BST_.

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


def sorted_array_to_bst(nums):
    def make(lo, hi):                       # builds from nums[lo..hi], both included
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = TreeNode(nums[mid])
        node.left = make(lo, mid - 1)
        node.right = make(mid + 1, hi)
        return node

    return make(0, len(nums) - 1)


assert to_list(sorted_array_to_bst([-10, -3, 0, 5, 9])) == [0, -10, 5, None, -3, None, 9]
assert to_list(sorted_array_to_bst([1, 3])) == [1, None, 3]
assert sorted_array_to_bst([]) is None
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

TreeNode* make_range(const vector<int>& nums, int lo, int hi) {
    if (lo > hi) return nullptr;
    int mid = (lo + hi) / 2;
    TreeNode* node = new TreeNode(nums[mid]);
    node->left = make_range(nums, lo, mid - 1);
    node->right = make_range(nums, mid + 1, hi);
    return node;
}

TreeNode* sorted_array_to_bst(const vector<int>& nums) {
    return make_range(nums, 0, (int)nums.size() - 1);
}
```

Each value becomes a node once, so the time is $O(n)$. The recursion goes $\log_2 n$ deep, so the extra space is $O(\log n)$.

## 7.2 Rebalancing a BST

What if the BST we are given has become badly unbalanced, even a chain? We rebuild it. The inorder walk gives all its values in sorted order, and the previous section turns a sorted list into a balanced BST. So rebalancing is the two steps glued together. This is exactly the problem _Balance a BST_.

```python
def inorder_values(root):
    out = []

    def visit(node):
        if node is None:
            return
        visit(node.left)
        out.append(node.val)
        visit(node.right)

    visit(root)
    return out


def balance_bst(root):
    return sorted_array_to_bst(inorder_values(root))


chain = build([1, None, 2, None, 3, None, 4])
assert to_list(balance_bst(chain)) == [2, 1, 3, None, None, None, 4]
assert balance_bst(None) is None
```

```cpp
void collect_inorder(TreeNode* node, vector<int>& out) {
    if (node == nullptr) return;
    collect_inorder(node->left, out);
    out.push_back(node->val);
    collect_inorder(node->right, out);
}

vector<int> inorder_values(TreeNode* root) {
    vector<int> out;
    collect_inorder(root, out);
    return out;
}

TreeNode* balance_bst(TreeNode* root) {
    return sorted_array_to_bst(inorder_values(root));
}
```

The time is $O(n)$ and the space is $O(n)$ for the list.

## 7.3 Trimming to a range

To **trim** a BST means to remove every node whose value is outside `[low, high]`, while keeping the shape of the rest as it was: a kept node stays below the same kept ancestors. The BST rule tells us what to do at each node. If the value is **below** `low`, then this node and its whole left subtree are too small and must go, but its right subtree may still contain good values, so we continue with the trimmed right subtree in its place. If the value is **above** `high`, we do the opposite and continue with the trimmed left subtree. If the value is in the range, we keep the node and trim both sides.

For `[3, 0, 4, None, 2, None, None, 1]` with `low = 1` and `high = 3`: the root `3` is fine; on the left, `0` is too small, so we replace it by its trimmed right subtree, which is `2` with its child `1`; on the right, `4` is too big and has no left subtree, so it disappears. The result is `[3, 2, None, 1]`. This is exactly the problem _Trim a BST_.

```python
def trim_bst(root, low, high):
    if root is None:
        return None
    if root.val < low:
        return trim_bst(root.right, low, high)
    if root.val > high:
        return trim_bst(root.left, low, high)
    root.left = trim_bst(root.left, low, high)
    root.right = trim_bst(root.right, low, high)
    return root


assert to_list(trim_bst(build([3, 0, 4, None, 2, None, None, 1]), 1, 3)) == [3, 2, None, 1]
assert to_list(trim_bst(build([1, 0, 2]), 1, 2)) == [1, None, 2]
assert trim_bst(build([5, 3, 8]), 10, 20) is None
```

```cpp
TreeNode* trim_bst(TreeNode* root, int low, int high) {
    if (root == nullptr) return nullptr;
    if (root->val < low) return trim_bst(root->right, low, high);
    if (root->val > high) return trim_bst(root->left, low, high);
    root->left = trim_bst(root->left, low, high);
    root->right = trim_bst(root->right, low, high);
    return root;
}
```

The time is $O(n)$ in the worst case and the space is $O(h)$.

## 7.4 Building from a preorder list

A BST is determined by its **preorder** traversal (root, left subtree, right subtree), even without the inorder list that we needed for general trees. The reason is that the inorder of a BST is just the sorted values, so we already know it. But there is an even shorter way that needs no sorting.

The first value of the preorder is the root. After it come the values of the left subtree (all smaller than the root), and then the values of the right subtree (all larger). We read the list from left to right with a pointer `pos`, and we give each recursive call an **upper bound**: the next value may only be used in this subtree if it is smaller than the bound. If the next value is larger than the bound (or the list is finished), this subtree is complete, so we return `None`. Otherwise we take the value as a node and build its left subtree with the bound set to the node's own value, and then its right subtree with the bound we received.

For `[8, 5, 1, 7, 10, 12]`: `8` is the root (bound infinity). Its left subtree takes values below 8: `5`, and below 5 comes `1`, then `7` is bigger than 5 so `5` is done with its left; with bound 8, `7` becomes the right child of `5`. Then `10` is above 8 and goes to the right subtree of `8`, with `12` as its right child. This is exactly the problem _Build a BST from Preorder_.

```python
def bst_from_preorder(preorder):
    pos = 0

    def build_below(bound):
        nonlocal pos
        if pos == len(preorder) or preorder[pos] > bound:
            return None
        node = TreeNode(preorder[pos])
        pos += 1
        node.left = build_below(node.val)
        node.right = build_below(bound)
        return node

    return build_below(float("inf"))


assert to_list(bst_from_preorder([8, 5, 1, 7, 10, 12])) == [8, 5, 10, 1, 7, None, 12]
assert to_list(bst_from_preorder([3, 2, 1])) == [3, 2, None, 1]
assert bst_from_preorder([]) is None
```

```cpp
TreeNode* build_below(const vector<int>& preorder, int& pos, long long bound) {
    if (pos == (int)preorder.size() || preorder[pos] > bound) return nullptr;
    TreeNode* node = new TreeNode(preorder[pos]);
    pos++;
    node->left = build_below(preorder, pos, node->val);
    node->right = build_below(preorder, pos, bound);
    return node;
}

TreeNode* bst_from_preorder(const vector<int>& preorder) {
    int pos = 0;
    return build_below(preorder, pos, LLONG_MAX);
}
```

Each value is used once, so the time is $O(n)$ and the space is $O(h)$.

## 7.5 Check yourself

1. Why do we pick the middle value as the root when building from a sorted list?
2. How can a badly shaped BST be rebalanced using two earlier ideas?
3. In trimming, what do we do with a node that is smaller than `low`, and why can we keep its right subtree?
4. In the preorder build, what does the `bound` tell us?

# Chapter 8. Repairing and measuring

## 8.1 Two values swapped by mistake

The last two problems are the hardest of the step. In the first, exactly **two nodes** of a BST have had their values swapped. We must put them back without changing the shape.

Think of the inorder list. A BST gives a sorted list; swapping two values in a sorted list creates "dips", places where a value is larger than the one after it. For the sorted list `1, 2, 3, 4, 5`, swapping `2` and `4` gives `1, 4, 3, 2, 5`. There are two dips: `4 > 3` and `3 > 2`. The first value of the first dip (`4`) and the second value of the last dip (`2`) are the two wrong nodes. If the swapped values were neighbours, like in `1, 3, 2, 4`, there is only one dip, `3 > 2`, and its two values are the wrong ones.

So the plan is: do an inorder walk, remembering the previous node. At every dip (previous larger than current), if it is the first dip then `first = previous`; in every dip set `second = current`. At the end, swap the values of `first` and `second`. For `[3, 1, 4, None, None, 2]` the inorder is `1, 3, 2, 4`: one dip `3 > 2`, so we swap those and get `[2, 1, 4, None, None, 3]`. This is exactly the problem _Recover a BST_.

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


def recover_tree(root):
    first = second = previous = None
    stack = []
    node = root
    while node is not None or stack:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if previous is not None and previous.val > node.val:
            if first is None:
                first = previous
            second = node
        previous = node
        node = node.right
    if first is not None:
        first.val, second.val = second.val, first.val
    return root


assert to_list(recover_tree(build([3, 1, 4, None, None, 2]))) == [2, 1, 4, None, None, 3]
assert to_list(recover_tree(build([1, 3, None, None, 2]))) == [3, 1, None, None, 2]
assert to_list(recover_tree(build([4, 2, 6, 1, 5, 3, 7]))) == [4, 2, 6, 1, 3, 5, 7]
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

TreeNode* recover_tree(TreeNode* root) {
    TreeNode* first = nullptr;
    TreeNode* second = nullptr;
    TreeNode* previous = nullptr;
    vector<TreeNode*> stack;
    TreeNode* node = root;
    while (node != nullptr || !stack.empty()) {
        while (node != nullptr) {
            stack.push_back(node);
            node = node->left;
        }
        node = stack.back();
        stack.pop_back();
        if (previous != nullptr && previous->val > node->val) {
            if (first == nullptr) first = previous;
            second = node;
        }
        previous = node;
        node = node->right;
    }
    if (first != nullptr) swap(first->val, second->val);
    return root;
}
```

The walk is $O(n)$ in time and $O(h)$ in space. (There is a trick called Morris traversal that brings the extra space down to $O(1)$, but the stack version is easier to get right.)

## 8.2 Largest BST inside a tree

In the last problem the tree is **not** necessarily a BST. We want the size of the largest **subtree** (a node with all its descendants) that is a valid BST. Checking every node with the range method of Chapter 4 would cost $O(n^2)$. A single pass is possible with the "answers flow up" pattern from the page on binary trees.

For each node we gather facts about its subtree from the two children: is it a BST, how many nodes does it have, what are its smallest and largest values. Then the node's own subtree is a BST exactly when both child subtrees are BSTs, the largest value on the left is smaller than the node, and the smallest value on the right is larger than the node. If so, its size is `left size + right size + 1`, and we update the best answer; its smallest value is `min(left smallest, node)` and its largest is `max(right largest, node)`. If not, it is not a BST, and none of the ancestors can be one either, since any BST that included this subtree would have to contain it as a valid BST.

An empty subtree is a BST of size 0. To make the comparisons work without extra cases, we give it a smallest value of $+\infty$ and a largest value of $-\infty$ (an "inverted" range), so that any node value passes the test.

For `[10, 5, 15, 1, 8, None, 7]`: the leaf subtrees are BSTs of size 1; the subtree at `5` has `1` on the left and `8` on the right, so it is a BST of size 3. The subtree at `15` has a right child `7`, which is smaller than 15, so it fails. Thus the root fails too and the answer is 3. This is exactly the problem _Largest BST Inside a Tree_.

```python
def largest_bst_subtree(root):
    best = 0

    def go(node):                          # returns (is_bst, size, smallest, largest)
        nonlocal best
        if node is None:
            return True, 0, float("inf"), float("-inf")
        left_ok, left_size, left_small, left_large = go(node.left)
        right_ok, right_size, right_small, right_large = go(node.right)
        if left_ok and right_ok and left_large < node.val < right_small:
            size = left_size + right_size + 1
            best = max(best, size)
            return True, size, min(left_small, node.val), max(right_large, node.val)
        return False, 0, 0, 0

    go(root)
    return best


assert largest_bst_subtree(build([10, 5, 15, 1, 8, None, 7])) == 3
assert largest_bst_subtree(build([2, 1, 3])) == 3
assert largest_bst_subtree(build([1, 2, 3])) == 1
assert largest_bst_subtree(None) == 0
```

```cpp
struct BSTInfo {
    bool ok;
    int size;
    long long smallest;
    long long largest;
};

BSTInfo largest_bst_go(TreeNode* node, int& best) {
    if (node == nullptr) return {true, 0, LLONG_MAX, LLONG_MIN};
    BSTInfo left = largest_bst_go(node->left, best);
    BSTInfo right = largest_bst_go(node->right, best);
    if (left.ok && right.ok && left.largest < node->val && node->val < right.smallest) {
        int size = left.size + right.size + 1;
        best = max(best, size);
        return {true, size, min(left.smallest, (long long)node->val), max(right.largest, (long long)node->val)};
    }
    return {false, 0, 0, 0};
}

int largest_bst_subtree(TreeNode* root) {
    int best = 0;
    largest_bst_go(root, best);
    return best;
}
```

Each node is visited once, so the time is $O(n)$ and the space is $O(h)$.

## 8.3 Check yourself

1. What does the inorder list of a BST with two swapped values look like?
2. In recover, why do we update `second` at every dip but `first` only at the first dip?
3. What facts does each node need from its subtrees to decide whether it is the root of a BST?
4. Why do we give an empty subtree the smallest value $+\infty$ and the largest value $-\infty$?
