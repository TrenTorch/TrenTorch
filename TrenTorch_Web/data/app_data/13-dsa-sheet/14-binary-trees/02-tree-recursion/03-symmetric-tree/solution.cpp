#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

static bool mirrorTrees(TreeNode* a, TreeNode* b) {
    if (a == nullptr && b == nullptr) return true;
    if (a == nullptr || b == nullptr || a->val != b->val) return false;
    return mirrorTrees(a->left, b->right) && mirrorTrees(a->right, b->left);
}

// O(n) time, O(h) space
bool isSymmetric(TreeNode* root) {
    return root == nullptr || mirrorTrees(root->left, root->right);
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
