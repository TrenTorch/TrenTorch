#include <bits/stdc++.h>
using namespace std;

// O(E * alpha(26)) time, O(1) space
bool equationsPossible(vector<string> equations) {
    vector<int> parent(26);
    iota(parent.begin(), parent.end(), 0);
    auto findRoot = [&](int a) {
        while (parent[a] != a) {
            parent[a] = parent[parent[a]];
            a = parent[a];
        }
        return a;
    };
    for (auto& eq : equations) {
        if (eq[1] == '=') {
            int ra = findRoot(eq[0] - 'a');
            int rb = findRoot(eq[3] - 'a');
            parent[ra] = rb;
        }
    }
    for (auto& eq : equations) {
        if (eq[1] == '!' && findRoot(eq[0] - 'a') == findRoot(eq[3] - 'a')) return false;
    }
    return true;
}

int main() {
    cout << boolalpha << equationsPossible(vector<string>{"a==b", "b!=a"}) << endl;
    return 0;
}
