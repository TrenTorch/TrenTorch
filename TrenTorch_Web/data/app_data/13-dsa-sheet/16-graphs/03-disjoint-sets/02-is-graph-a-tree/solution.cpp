#include <bits/stdc++.h>
using namespace std;

// O(E * alpha(N)) time, O(N) space
bool validTree(long long n, vector<vector<long long>> edges) {
    if (n == 0 || (long long)edges.size() != n - 1) return false;
    int N = n;
    vector<int> parent(N), sz(N, 1);
    iota(parent.begin(), parent.end(), 0);
    auto findRoot = [&](int a) {
        while (parent[a] != a) {
            parent[a] = parent[parent[a]];
            a = parent[a];
        }
        return a;
    };
    for (auto& e : edges) {
        int a = e[0], b = e[1];
        int ra = findRoot(a), rb = findRoot(b);
        if (ra == rb) return false;
        if (sz[ra] < sz[rb]) swap(ra, rb);
        parent[rb] = ra;
        sz[ra] += sz[rb];
    }
    return true;
}

int main() {
    cout << boolalpha << validTree(5, vector<vector<long long>>{vector<long long>{0, 1}, vector<long long>{0, 2}, vector<long long>{0, 3}, vector<long long>{1, 4}}) << endl;
    return 0;
}
