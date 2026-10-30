#include <bits/stdc++.h>
using namespace std;

// O(n + m) time, O(n + m) space (m = number of edges)
bool hasCycleUndirected(long long n, vector<vector<long long>> edges) {
    vector<vector<pair<long long, long long>>> adj(n);
    for (long long i = 0; i < (long long)edges.size(); i++) {
        long long a = edges[i][0];
        long long b = edges[i][1];
        if (a == b) return true;
        adj[a].push_back({b, i});
        adj[b].push_back({a, i});
    }
    vector<bool> seen(n, false);
    for (long long start = 0; start < n; start++) {
        if (seen[start]) continue;
        seen[start] = true;
        vector<pair<long long, long long>> stack = {{start, -1}};
        while (!stack.empty()) {
            auto [node, via] = stack.back();
            stack.pop_back();
            for (const auto& [nxt, edgeId] : adj[node]) {
                if (edgeId == via) continue;
                if (seen[nxt]) return true;
                seen[nxt] = true;
                stack.push_back({nxt, edgeId});
            }
        }
    }
    return false;
}

int main() {
    cout << boolalpha << hasCycleUndirected(4, vector<vector<long long>>{vector<long long>{0, 1}, vector<long long>{1, 2}, vector<long long>{2, 0}, vector<long long>{3, 3}}) << endl;
    return 0;
}
