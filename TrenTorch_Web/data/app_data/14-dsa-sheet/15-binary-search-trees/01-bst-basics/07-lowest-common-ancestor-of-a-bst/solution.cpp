#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(h) time, O(1) space (h = tree height)
TreeNode* lcaBst(TreeNode* root, long long p, long long q) {
    TreeNode* node = root;
    while (node) {
        if (p < node->val && q < node->val) {
            node = node->left;
        } else if (p > node->val && q > node->val) {
            node = node->right;
        } else {
            return node;
        }
    }
    return nullptr;
}

int main() {
    return 0;
}
