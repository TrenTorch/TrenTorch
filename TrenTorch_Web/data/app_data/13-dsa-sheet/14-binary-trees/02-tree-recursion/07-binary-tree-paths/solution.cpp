#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x = 0, TreeNode* l = nullptr, TreeNode* r = nullptr) : val(x), left(l), right(r) {}
};

static void collectPaths(TreeNode* node, vector<string>& path, vector<string>& out) {
    if (node == nullptr) return;
    path.push_back(to_string(node->val));
    if (node->left == nullptr && node->right == nullptr) {
        string joined;
        for (size_t i = 0; i < path.size(); ++i) {
            if (i > 0) joined += "->";
            joined += path[i];
        }
        out.push_back(joined);
    } else {
        collectPaths(node->left, path, out);
        collectPaths(node->right, path, out);
    }
    path.pop_back();
}

// O(n * h) time, O(h) extra space besides the output
vector<string> rootToLeafPaths(TreeNode* root) {
    vector<string> out;
    vector<string> path;
    collectPaths(root, path, out);
    return out;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
