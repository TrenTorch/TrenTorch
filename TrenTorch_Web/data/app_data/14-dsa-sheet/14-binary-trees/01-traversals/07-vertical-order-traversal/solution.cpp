#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n log n) time, O(n) space
vector<vector<long long>> verticalOrder(TreeNode* root) {
    vector<vector<long long>> out;
    if (!root) return out;
    map<long long, vector<pair<long long, long long>>> columns;
    queue<tuple<TreeNode*, long long, long long>> q;
    q.push({root, 0, 0});
    while (!q.empty()) {
        auto [node, row, col] = q.front();
        q.pop();
        columns[col].push_back({row, node->val});
        if (node->left) q.push({node->left, row + 1, col - 1});
        if (node->right) q.push({node->right, row + 1, col + 1});
    }
    for (auto& entry : columns) {
        auto& items = entry.second;
        sort(items.begin(), items.end());
        vector<long long> values;
        for (auto& item : items) values.push_back(item.second);
        out.push_back(values);
    }
    return out;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
