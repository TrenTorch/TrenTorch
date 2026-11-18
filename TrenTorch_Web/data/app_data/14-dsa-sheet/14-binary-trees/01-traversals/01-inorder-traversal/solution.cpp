#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n) time, O(h) space where h is the tree height
vector<long long> inorderTraversal(TreeNode* root) {
    vector<long long> out;
    vector<TreeNode*> stack;
    TreeNode* node = root;
    while (node || !stack.empty()) {
        while (node) {
            stack.push_back(node);
            node = node->left;
        }
        node = stack.back();
        stack.pop_back();
        out.push_back(node->val);
        node = node->right;
    }
    return out;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
