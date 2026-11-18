#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(E * alpha(E)) time, O(E) space
vector<long long> findRedundantConnection(vector<vector<long long>> edges) {
    int N = edges.size() + 2;
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
        if (ra == rb) return {a, b};
        if (sz[ra] < sz[rb]) swap(ra, rb);
        parent[rb] = ra;
        sz[ra] += sz[rb];
    }
    return {};
}

int main() {
    cout << findRedundantConnection(vector<vector<long long>>{vector<long long>{1, 2}, vector<long long>{1, 3}, vector<long long>{2, 3}}) << endl;
    return 0;
}
