#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

static long long depthOf(TreeNode* node) {
    if (node == nullptr) return 0;
    return 1 + max(depthOf(node->left), depthOf(node->right));
}

// O(n) time, O(h) space
long long maxDepth(TreeNode* root) {
    return depthOf(root);
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
