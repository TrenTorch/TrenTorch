#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

static TreeNode* buildBalanced(const vector<long long>& values, long long lo, long long hi) {
    if (lo > hi) return nullptr;
    long long mid = (lo + hi) / 2;
    TreeNode* left = buildBalanced(values, lo, mid - 1);
    TreeNode* right = buildBalanced(values, mid + 1, hi);
    return new TreeNode((int)values[mid], left, right);
}

// O(n) time, O(n) space (inorder value list plus rebuilt tree)
TreeNode* balanceBst(TreeNode* root) {
    vector<long long> values;
    stack<TreeNode*> st;
    TreeNode* node = root;
    while (node || !st.empty()) {
        while (node) {
            st.push(node);
            node = node->left;
        }
        node = st.top();
        st.pop();
        values.push_back(node->val);
        node = node->right;
    }
    return buildBalanced(values, 0, (long long)values.size() - 1);
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
