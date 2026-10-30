#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

static long long checkHeight(TreeNode* node) {
    if (node == nullptr) return 0;
    long long left = checkHeight(node->left);
    if (left == -1) return -1;
    long long right = checkHeight(node->right);
    if (right == -1 || llabs(left - right) > 1) return -1;
    return 1 + max(left, right);
}

// O(n) time, O(h) space
bool isBalanced(TreeNode* root) {
    return checkHeight(root) != -1;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
