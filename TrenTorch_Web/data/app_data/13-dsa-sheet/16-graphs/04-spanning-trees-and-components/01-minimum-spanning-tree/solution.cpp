#include <bits/stdc++.h>
using namespace std;

// O(E log E) time, O(N + E) space
long long mstWeight(long long n, vector<vector<long long>> edges) {
    stable_sort(edges.begin(), edges.end(), [](const vector<long long>& x, const vector<long long>& y) {
        return x[2] < y[2];
    });
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
    long long total = 0;
    long long taken = 0;
    for (auto& e : edges) {
        int ra = findRoot(e[0]), rb = findRoot(e[1]);
        if (ra != rb) {
            if (sz[ra] < sz[rb]) swap(ra, rb);
            parent[rb] = ra;
            sz[ra] += sz[rb];
            total += e[2];
            taken++;
        }
    }
    return taken == n - 1 ? total : -1;
}

int main() {
    cout << mstWeight(4, vector<vector<long long>>{vector<long long>{0, 1, 1}, vector<long long>{1, 2, 2}, vector<long long>{2, 3, 3}, vector<long long>{0, 3, 10}, vector<long long>{0, 2, 5}}) << endl;
    return 0;
}
