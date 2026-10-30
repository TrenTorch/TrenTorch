#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n) time, O(n) space
long long burnTime(TreeNode* root, long long start) {
    unordered_map<TreeNode*, TreeNode*> parent;
    TreeNode* origin = nullptr;
    vector<pair<TreeNode*, TreeNode*>> stack;
    stack.push_back({root, nullptr});
    while (!stack.empty()) {
        auto [node, par] = stack.back();
        stack.pop_back();
        parent[node] = par;
        if (node->val == start) origin = node;
        if (node->left) stack.push_back({node->left, node});
        if (node->right) stack.push_back({node->right, node});
    }
    unordered_set<TreeNode*> seen;
    seen.insert(origin);
    deque<TreeNode*> frontier;
    frontier.push_back(origin);
    long long minutes = -1;
    while (!frontier.empty()) {
        minutes += 1;
        size_t count = frontier.size();
        for (size_t i = 0; i < count; ++i) {
            TreeNode* node = frontier.front();
            frontier.pop_front();
            TreeNode* neighbours[3] = {node->left, node->right, parent[node]};
            for (TreeNode* nxt : neighbours) {
                if (nxt != nullptr && seen.count(nxt) == 0) {
                    seen.insert(nxt);
                    frontier.push_back(nxt);
                }
            }
        }
    }
    return minutes;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
