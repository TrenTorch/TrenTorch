#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

static bool hasPathFrom(TreeNode* node, long long target) {
    if (node == nullptr) return false;
    if (node->left == nullptr && node->right == nullptr) return node->val == target;
    long long rest = target - node->val;
    return hasPathFrom(node->left, rest) || hasPathFrom(node->right, rest);
}

// O(n) time, O(h) space
bool hasPathSum(TreeNode* root, long long target) {
    return hasPathFrom(root, target);
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
