#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n) time, O(h) space where h is the tree height
vector<long long> preorderTraversal(TreeNode* root) {
    vector<long long> out;
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

int main() {
    // Call it here and print the result to try it.
    return 0;
}
