#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n) time, O(n) space
vector<vector<long long>> zigzagLevelOrder(TreeNode* root) {
    vector<vector<long long>> out;
    queue<TreeNode*> q;
    if (root) q.push(root);
    bool leftToRight = true;
    while (!q.empty()) {
        vector<long long> level;
        size_t count = q.size();
        for (size_t i = 0; i < count; ++i) {
            TreeNode* node = q.front();
            q.pop();
            level.push_back(node->val);
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
        if (!leftToRight) reverse(level.begin(), level.end());
        out.push_back(level);
        leftToRight = !leftToRight;
    }
    return out;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
