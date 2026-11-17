#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n log n) time, O(n) space
vector<long long> distanceK(TreeNode* root, long long target, long long k) {
    unordered_map<TreeNode*, TreeNode*> parent;
    TreeNode* start = nullptr;
    vector<pair<TreeNode*, TreeNode*>> stack;
    stack.push_back({root, nullptr});
    while (!stack.empty()) {
        auto [node, par] = stack.back();
        stack.pop_back();
        parent[node] = par;
        if (node->val == target) start = node;
        if (node->left) stack.push_back({node->left, node});
        if (node->right) stack.push_back({node->right, node});
    }
    unordered_set<TreeNode*> seen;
    seen.insert(start);
    deque<TreeNode*> frontier;
    frontier.push_back(start);
    for (long long step = 0; step < k; ++step) {
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
    vector<long long> out;
    for (TreeNode* node : frontier) out.push_back(node->val);
    sort(out.begin(), out.end());
    return out;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
