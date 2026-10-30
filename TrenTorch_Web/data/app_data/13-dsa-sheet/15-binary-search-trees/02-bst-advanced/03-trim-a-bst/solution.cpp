#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n) time, O(h) space (h = tree height, recursion depth)
TreeNode* trimBst(TreeNode* root, long long low, long long high) {
    if (root == nullptr) return nullptr;
    if (root->val < low) return trimBst(root->right, low, high);
    if (root->val > high) return trimBst(root->left, low, high);
    root->left = trimBst(root->left, low, high);
    root->right = trimBst(root->right, low, high);
    return root;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
