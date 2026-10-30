#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n) time, O(h) space (reverse inorder with explicit stack)
TreeNode* convertBst(TreeNode* root) {
    long long total = 0;
    stack<TreeNode*> st;
    TreeNode* node = root;
    while (node || !st.empty()) {
        while (node) {
            st.push(node);
            node = node->right;
        }
        node = st.top();
        st.pop();
        total += node->val;
        node->val = (int)total;
        node = node->left;
    }
    return root;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
