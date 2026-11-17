#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

struct BstInfo {
    long long size;
    long long low;
    long long high;
};

const long long BST_INF = (long long)4e18;

BstInfo goBst(TreeNode* node, long long& best) {
    if (node == nullptr) return {0, BST_INF, -BST_INF};
    BstInfo left = goBst(node->left, best);
    BstInfo right = goBst(node->right, best);
    if (left.size >= 0 && right.size >= 0 && left.high < node->val && node->val < right.low) {
        long long size = left.size + right.size + 1;
        best = max(best, size);
        return {size, min(left.low, (long long)node->val), max(right.high, (long long)node->val)};
    }
    return {-1, -BST_INF, BST_INF};
}

// O(n) time, O(h) space (h = tree height, for the recursion stack)
long long largestBstSubtree(TreeNode* root) {
    long long best = 0;
    goBst(root, best);
    return best;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
