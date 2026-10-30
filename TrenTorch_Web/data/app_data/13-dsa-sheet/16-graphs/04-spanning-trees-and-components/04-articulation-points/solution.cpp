#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

struct DfsFrame {
    int node, parent, i;
};

// O(V + E) time, O(V + E) space (iterative Tarjan articulation-point search)
vector<long long> articulationPoints(long long n, vector<vector<long long>> edges) {
    int N = n;
    vector<vector<int>> adj(N);
    for (auto& e : edges) {
        int a = e[0], b = e[1];
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    vector<int> disc(N, -1), low(N, 0);
    vector<bool> isCut(N, false);
    int timer = 0;
    for (int root = 0; root < N; root++) {
        if (disc[root] != -1) continue;
        disc[root] = low[root] = timer++;
        int rootChildren = 0;
        vector<DfsFrame> stk = {{root, -1, 0}};
        while (!stk.empty()) {
            DfsFrame f = stk.back();
            stk.pop_back();
            int node = f.node, parent = f.parent, i = f.i;
            if (i < (int)adj[node].size()) {
                stk.push_back({node, parent, i + 1});
                int nxt = adj[node][i];
                if (nxt == parent) continue;
                if (disc[nxt] == -1) {
                    disc[nxt] = low[nxt] = timer++;
                    if (node == root) rootChildren++;
                    stk.push_back({nxt, node, 0});
                } else {
                    low[node] = min(low[node], disc[nxt]);
                }
            } else if (parent != -1) {
                low[parent] = min(low[parent], low[node]);
                if (parent != root && low[node] >= disc[parent]) isCut[parent] = true;
            }
        }
        if (rootChildren >= 2) isCut[root] = true;
    }
    vector<long long> res;
    for (int v = 0; v < N; v++) {
        if (isCut[v]) res.push_back(v);
    }
    return res;
}

int main() {
    cout << articulationPoints(5, vector<vector<long long>>{vector<long long>{0, 1}, vector<long long>{1, 2}, vector<long long>{2, 0}, vector<long long>{1, 3}, vector<long long>{3, 4}}) << endl;
    return 0;
}
