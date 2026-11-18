#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(h) time, O(1) space (h = tree height)
long long closestValue(TreeNode* root, long long target) {
    if (root == nullptr) return 0;
    long long best = root->val;
    TreeNode* node = root;
    while (node) {
        long long cur = node->val;
        long long curDiff = llabs(cur - target);
        long long bestDiff = llabs(best - target);
        if (curDiff < bestDiff || (curDiff == bestDiff && cur < best)) best = cur;
        node = target < cur ? node->left : node->right;
    }
    return best;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
