#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

static long long heightAndBest(TreeNode* node, long long& best) {
    if (node == nullptr) return 0;
    long long left = heightAndBest(node->left, best);
    long long right = heightAndBest(node->right, best);
    best = max(best, left + right);
    return 1 + max(left, right);
}

// O(n) time, O(h) space
long long diameter(TreeNode* root) {
    long long best = 0;
    heightAndBest(root, best);
    return best;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
