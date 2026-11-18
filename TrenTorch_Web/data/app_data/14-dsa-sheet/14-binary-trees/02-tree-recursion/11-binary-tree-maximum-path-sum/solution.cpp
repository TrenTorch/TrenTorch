#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

static long long gainOf(TreeNode* node, long long& best) {
    if (node == nullptr) return 0;
    long long left = max(0LL, gainOf(node->left, best));
    long long right = max(0LL, gainOf(node->right, best));
    best = max(best, (long long)node->val + left + right);
    return node->val + max(left, right);
}

// O(n) time, O(h) space
long long maxPathSum(TreeNode* root) {
    if (root == nullptr) return 0;
    long long best = root->val;
    gainOf(root, best);
    return best;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
