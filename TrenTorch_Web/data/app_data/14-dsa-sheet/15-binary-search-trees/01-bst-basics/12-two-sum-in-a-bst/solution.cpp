#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// Yields node values in increasing order (inorder traversal, lazily).
struct AscendingIter {
    stack<TreeNode*> st;
    explicit AscendingIter(TreeNode* root) { pushLeft(root); }
    void pushLeft(TreeNode* node) {
        while (node) {
            st.push(node);
            node = node->left;
        }
    }
    bool next(long long& out) {
        if (st.empty()) return false;
        TreeNode* node = st.top();
        st.pop();
        out = node->val;
        pushLeft(node->right);
        return true;
    }
};

// Yields node values in decreasing order (reverse inorder, lazily).
struct DescendingIter {
    stack<TreeNode*> st;
    explicit DescendingIter(TreeNode* root) { pushRight(root); }
    void pushRight(TreeNode* node) {
        while (node) {
            st.push(node);
            node = node->right;
        }
    }
    bool next(long long& out) {
        if (st.empty()) return false;
        TreeNode* node = st.top();
        st.pop();
        out = node->val;
        pushRight(node->left);
        return true;
    }
};

// O(n) time, O(h) space (two lazy traversals with explicit stacks)
bool findTarget(TreeNode* root, long long k) {
    AscendingIter up(root);
    DescendingIter down(root);
    long long lo = 0;
    long long hi = 0;
    bool hasLo = up.next(lo);
    bool hasHi = down.next(hi);
    while (hasLo && hasHi && lo < hi) {
        long long total = lo + hi;
        if (total == k) return true;
        if (total < k) {
            hasLo = up.next(lo);
        } else {
            hasHi = down.next(hi);
        }
    }
    return false;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
