#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(V + E) time, O(V + E) space (leaf trimming)
vector<long long> minHeightTrees(long long n, vector<vector<long long>> edges) {
    if (n <= 2) {
        vector<long long> res;
        for (long long i = 0; i < n; i++) res.push_back(i);
        return res;
    }
    int N = n;
    vector<vector<int>> adj(N);
    for (auto& e : edges) {
        int a = e[0], b = e[1];
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    vector<int> degree(N);
    for (int v = 0; v < N; v++) degree[v] = adj[v].size();
    vector<int> leaves;
    for (int v = 0; v < N; v++) {
        if (degree[v] == 1) leaves.push_back(v);
    }
    long long remaining = N;
    while (remaining > 2) {
        remaining -= leaves.size();
        vector<int> nxt;
        for (int leaf : leaves) {
            for (int other : adj[leaf]) {
                degree[other]--;
                if (degree[other] == 1) nxt.push_back(other);
            }
        }
        leaves = nxt;
    }
    sort(leaves.begin(), leaves.end());
    return vector<long long>(leaves.begin(), leaves.end());
}

int main() {
    cout << minHeightTrees(6, vector<vector<long long>>{vector<long long>{3, 0}, vector<long long>{3, 1}, vector<long long>{3, 2}, vector<long long>{3, 4}, vector<long long>{5, 4}}) << endl;
    return 0;
}
