#include <bits/stdc++.h>
using namespace std;

// O((V + E) log V) time, O(V + E) space
long long countShortestPaths(long long n, vector<vector<long long>> roads) {
    const long long MOD = 1000000007LL;
    int N = n;
    vector<vector<pair<int, long long>>> adj(N);
    for (auto& r : roads) {
        int a = r[0], b = r[1];
        long long t = r[2];
        adj[a].push_back({b, t});
        adj[b].push_back({a, t});
    }
    const long long INF = LLONG_MAX / 4;
    vector<long long> dist(N, INF), ways(N, 0);
    dist[0] = 0;
    ways[0] = 1;
    using State = pair<long long, int>;
    priority_queue<State, vector<State>, greater<State>> heap;
    heap.push({0, 0});
    while (!heap.empty()) {
        auto [d, u] = heap.top();
        heap.pop();
        if (d > dist[u]) continue;
        for (auto [v, t] : adj[u]) {
            long long nd = d + t;
            if (nd < dist[v]) {
                dist[v] = nd;
                ways[v] = ways[u];
                heap.push({nd, v});
            } else if (nd == dist[v]) {
                ways[v] = (ways[v] + ways[u]) % MOD;
            }
        }
    }
    return ways[N - 1] % MOD;
}

int main() {
    cout << countShortestPaths(4, vector<vector<long long>>{vector<long long>{0, 1, 1}, vector<long long>{0, 2, 1}, vector<long long>{1, 3, 1}, vector<long long>{2, 3, 1}}) << endl;
    return 0;
}
