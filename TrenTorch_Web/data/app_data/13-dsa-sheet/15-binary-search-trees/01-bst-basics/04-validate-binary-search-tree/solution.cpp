#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

static bool checkBst(TreeNode* node, long long low, long long high) {
    if (node == nullptr) return true;
    if (!(low < node->val && node->val < high)) return false;
    return checkBst(node->left, low, node->val) && checkBst(node->right, node->val, high);
}

// O(n) time, O(h) space (h = tree height, recursion depth)
bool isValidBst(TreeNode* root) {
    return checkBst(root, LLONG_MIN, LLONG_MAX);
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
