#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n) time, O(n) space
vector<long long> rightSideView(TreeNode* root) {
    vector<long long> out;
    queue<TreeNode*> q;
    if (root) q.push(root);
    while (!q.empty()) {
        size_t count = q.size();
        long long last = 0;
        for (size_t i = 0; i < count; ++i) {
            TreeNode* node = q.front();
            q.pop();
            last = node->val;
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
        out.push_back(last);
    }
    return out;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
