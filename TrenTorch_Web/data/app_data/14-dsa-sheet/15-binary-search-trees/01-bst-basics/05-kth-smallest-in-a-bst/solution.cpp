#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(h + k) time, O(h) space (explicit inorder stack)
long long kthSmallestBst(TreeNode* root, long long k) {
    stack<TreeNode*> st;
    TreeNode* node = root;
    while (node || !st.empty()) {
        while (node) {
            st.push(node);
            node = node->left;
        }
        node = st.top();
        st.pop();
        k--;
        if (k == 0) return node->val;
        node = node->right;
    }
    return 0;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
