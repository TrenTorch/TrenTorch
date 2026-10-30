#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O((n + m) log n) time, O(n + m) space (m = number of edges)
vector<long long> shortestDistances(long long n, vector<vector<long long>> edges, long long source) {
    vector<vector<pair<long long, long long>>> adj(n);
    for (const auto& e : edges) adj[e[0]].push_back({e[1], e[2]});
    const long long INF = LLONG_MAX / 4;
    vector<long long> dist(n, INF);
    dist[source] = 0;
    using State = pair<long long, long long>;
    priority_queue<State, vector<State>, greater<State>> heap;
    heap.push({0, source});
    while (!heap.empty()) {
        auto [d, u] = heap.top();
        heap.pop();
        if (d > dist[u]) continue;
        for (const auto& [v, w] : adj[u]) {
            if (d + w < dist[v]) {
                dist[v] = d + w;
                heap.push({dist[v], v});
            }
        }
    }
    vector<long long> result(n);
    for (long long i = 0; i < n; i++) {
        result[i] = dist[i] < INF ? dist[i] : -1;
    }
    return result;
}

int main() {
    cout << shortestDistances(3, vector<vector<long long>>{vector<long long>{0, 1, 4}, vector<long long>{0, 2, 1}, vector<long long>{2, 1, 2}}, 0) << endl;
    return 0;
}
