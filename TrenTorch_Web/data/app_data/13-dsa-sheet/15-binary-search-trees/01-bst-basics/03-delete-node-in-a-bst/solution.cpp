#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(h) time, O(h) space (h = tree height, recursion depth)
TreeNode* deleteNode(TreeNode* root, long long key) {
    if (root == nullptr) return nullptr;
    if (key < root->val) {
        root->left = deleteNode(root->left, key);
    } else if (key > root->val) {
        root->right = deleteNode(root->right, key);
    } else {
        if (root->left == nullptr) return root->right;
        if (root->right == nullptr) return root->left;
        TreeNode* successor = root->right;
        while (successor->left) successor = successor->left;
        root->val = successor->val;
        root->right = deleteNode(root->right, successor->val);
    }
    return root;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
