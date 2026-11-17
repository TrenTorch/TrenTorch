#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

static vector<long long> inorderValues(TreeNode* root) {
    vector<long long> out;
    stack<TreeNode*> st;
    TreeNode* node = root;
    while (node || !st.empty()) {
        while (node) {
            st.push(node);
            node = node->left;
        }
        node = st.top();
        st.pop();
        out.push_back(node->val);
        node = node->right;
    }
    return out;
}

// O(n + m) time, O(n + m) space (two sorted inorder lists, then a linear merge)
vector<long long> mergeBsts(TreeNode* root1, TreeNode* root2) {
    vector<long long> a = inorderValues(root1);
    vector<long long> b = inorderValues(root2);
    vector<long long> out;
    out.reserve(a.size() + b.size());
    size_t i = 0;
    size_t j = 0;
    while (i < a.size() && j < b.size()) {
        if (a[i] <= b[j]) {
            out.push_back(a[i]);
            i++;
        } else {
            out.push_back(b[j]);
            j++;
        }
    }
    while (i < a.size()) out.push_back(a[i++]);
    while (j < b.size()) out.push_back(b[j++]);
    return out;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
