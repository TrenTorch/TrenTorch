#include <bits/stdc++.h>
using namespace std;

// O(n + m) time, O(n + m) space (m = number of edges)
bool isBipartite(long long n, vector<vector<long long>> edges) {
    vector<vector<long long>> adj(n);
    for (const auto& e : edges) {
        adj[e[0]].push_back(e[1]);
        adj[e[1]].push_back(e[0]);
    }
    vector<long long> color(n, -1);
    for (long long start = 0; start < n; start++) {
        if (color[start] != -1) continue;
        color[start] = 0;
        deque<long long> queue = {start};
        while (!queue.empty()) {
            long long node = queue.front();
            queue.pop_front();
            for (long long nxt : adj[node]) {
                if (color[nxt] == -1) {
                    color[nxt] = 1 - color[node];
                    queue.push_back(nxt);
                } else if (color[nxt] == color[node]) {
                    return false;
                }
            }
        }
    }
    return true;
}

int main() {
    cout << boolalpha << isBipartite(4, vector<vector<long long>>{vector<long long>{0, 1}, vector<long long>{1, 2}, vector<long long>{2, 3}, vector<long long>{3, 0}}) << endl;
    return 0;
}
