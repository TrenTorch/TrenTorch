#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(h) time, O(1) space (h = tree height)
TreeNode* searchBst(TreeNode* root, long long val) {
    TreeNode* node = root;
    while (node && node->val != val) {
        node = val < node->val ? node->left : node->right;
    }
    return node;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
