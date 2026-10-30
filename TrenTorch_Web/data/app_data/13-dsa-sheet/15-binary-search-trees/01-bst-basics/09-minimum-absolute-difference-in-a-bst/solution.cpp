#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n) time, O(h) space (explicit inorder stack)
long long minDiffBst(TreeNode* root) {
    long long best = LLONG_MAX;
    bool hasPrev = false;
    long long prev = 0;
    stack<TreeNode*> st;
    TreeNode* node = root;
    while (node || !st.empty()) {
        while (node) {
            st.push(node);
            node = node->left;
        }
        node = st.top();
        st.pop();
        if (hasPrev) best = min(best, node->val - prev);
        prev = node->val;
        hasPrev = true;
        node = node->right;
    }
    return best;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
