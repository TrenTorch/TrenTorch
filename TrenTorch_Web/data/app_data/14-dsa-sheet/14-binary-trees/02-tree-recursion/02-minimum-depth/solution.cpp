#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n) time, O(n) space
long long minDepth(TreeNode* root) {
    if (root == nullptr) return 0;
    queue<pair<TreeNode*, long long>> q;
    q.push({root, 1});
    while (!q.empty()) {
        auto [node, depth] = q.front();
        q.pop();
        if (!node->left && !node->right) return depth;
        if (node->left) q.push({node->left, depth + 1});
        if (node->right) q.push({node->right, depth + 1});
    }
    return 0;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
