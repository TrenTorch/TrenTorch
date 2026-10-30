#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n) time, O(h) space
TreeNode* invertTree(TreeNode* root) {
    if (root == nullptr) return nullptr;
    TreeNode* newLeft = invertTree(root->right);
    TreeNode* newRight = invertTree(root->left);
    root->left = newLeft;
    root->right = newRight;
    return root;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
