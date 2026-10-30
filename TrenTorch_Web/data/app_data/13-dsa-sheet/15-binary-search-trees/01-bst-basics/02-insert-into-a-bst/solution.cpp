#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(h) time, O(1) space (h = tree height)
TreeNode* insertIntoBst(TreeNode* root, long long val) {
    if (root == nullptr) return new TreeNode((int)val);
    TreeNode* node = root;
    while (true) {
        if (val < node->val) {
            if (node->left == nullptr) {
                node->left = new TreeNode((int)val);
                break;
            }
            node = node->left;
        } else {
            if (node->right == nullptr) {
                node->right = new TreeNode((int)val);
                break;
            }
            node = node->right;
        }
    }
    return root;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
