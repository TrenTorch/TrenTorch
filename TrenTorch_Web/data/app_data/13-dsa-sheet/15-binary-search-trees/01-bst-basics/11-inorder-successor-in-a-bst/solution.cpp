#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

// O(h) time, O(1) space (h = tree height)
TreeNode* inorderSuccessor(TreeNode* root, long long p) {
    TreeNode* answer = nullptr;
    TreeNode* node = root;
    while (node) {
        if (node->val > p) {
            answer = node;
            node = node->left;
        } else {
            node = node->right;
        }
    }
    return answer;
}

int main() {
    return 0;
}
