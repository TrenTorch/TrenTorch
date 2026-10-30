#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n) time, O(1) extra space
TreeNode* flattenTree(TreeNode* root) {
    TreeNode* node = root;
    while (node != nullptr) {
        if (node->left != nullptr) {
            TreeNode* tail = node->left;
            while (tail->right != nullptr) tail = tail->right;
            tail->right = node->right;
            node->right = node->left;
            node->left = nullptr;
        }
        node = node->right;
    }
    return root;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
