#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(h) time, O(1) space (h = tree height)
vector<long long> floorAndCeilBst(TreeNode* root, long long x) {
    long long floorVal = -1;
    long long ceilVal = -1;
    TreeNode* node = root;
    while (node) {
        if (node->val == x) return {x, x};
        if (node->val < x) {
            floorVal = node->val;
            node = node->right;
        } else {
            ceilVal = node->val;
            node = node->left;
        }
    }
    return {floorVal, ceilVal};
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
