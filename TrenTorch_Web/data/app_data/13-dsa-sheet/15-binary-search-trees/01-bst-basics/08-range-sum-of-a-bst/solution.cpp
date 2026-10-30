#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n) time, O(h) space (h = tree height, recursion depth)
long long rangeSumBst(TreeNode* root, long long low, long long high) {
    if (root == nullptr) return 0;
    if (root->val < low) return rangeSumBst(root->right, low, high);
    if (root->val > high) return rangeSumBst(root->left, low, high);
    return root->val + rangeSumBst(root->left, low, high) + rangeSumBst(root->right, low, high);
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
