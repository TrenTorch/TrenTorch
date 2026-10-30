#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n) time, O(h) space (explicit inorder stack)
TreeNode* recoverTree(TreeNode* root) {
    TreeNode* first = nullptr;
    TreeNode* second = nullptr;
    TreeNode* prev = nullptr;
    stack<TreeNode*> st;
    TreeNode* node = root;
    while (node || !st.empty()) {
        while (node) {
            st.push(node);
            node = node->left;
        }
        node = st.top();
        st.pop();
        if (prev != nullptr && prev->val > node->val) {
            if (first == nullptr) first = prev;
            second = node;
        }
        prev = node;
        node = node->right;
    }
    swap(first->val, second->val);
    return root;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
