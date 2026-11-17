#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(n) time, O(n) space (BFS queue holds at most one level)
long long widthOfTree(TreeNode* root) {
    if (root == nullptr) return 0;
    long long best = 0;
    deque<pair<TreeNode*, long long>> queue;
    queue.push_back({root, 0});
    while (!queue.empty()) {
        long long first = queue.front().second;
        long long last = 0;
        size_t levelSize = queue.size();
        for (size_t i = 0; i < levelSize; i++) {
            auto [node, index] = queue.front();
            queue.pop_front();
            long long rel = index - first;
            last = rel;
            if (node->left) queue.push_back({node->left, 2 * rel + 1});
            if (node->right) queue.push_back({node->right, 2 * rel + 2});
        }
        best = max(best, last + 1);
    }
    return best;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
