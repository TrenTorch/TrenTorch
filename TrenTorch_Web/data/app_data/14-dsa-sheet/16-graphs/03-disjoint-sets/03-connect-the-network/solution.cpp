#include <bits/stdc++.h>
using namespace std;

// O(E * alpha(N)) time, O(N) space
long long makeConnected(long long n, vector<vector<long long>> connections) {
    if ((long long)connections.size() < n - 1) return -1;
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
    long long components = n;
    for (auto& c : connections) {
        int ra = findRoot(c[0]), rb = findRoot(c[1]);
        if (ra != rb) {
            if (sz[ra] < sz[rb]) swap(ra, rb);
            parent[rb] = ra;
            sz[ra] += sz[rb];
            components--;
        }
    }
    return components - 1;
}

int main() {
    cout << makeConnected(4, vector<vector<long long>>{vector<long long>{0, 1}, vector<long long>{0, 2}, vector<long long>{1, 2}}) << endl;
    return 0;
}
