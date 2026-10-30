#include <bits/stdc++.h>
using namespace std;

// O(n + m) time, O(n + m) space (m = number of edges)
bool validPath(long long n, vector<vector<long long>> edges, long long source, long long destination) {
    vector<vector<long long>> adj(n);
    for (const auto& e : edges) {
        adj[e[0]].push_back(e[1]);
        adj[e[1]].push_back(e[0]);
    }
    vector<bool> seen(n, false);
    seen[source] = true;
    vector<long long> stack = {source};
    while (!stack.empty()) {
        long long node = stack.back();
        stack.pop_back();
        if (node == destination) return true;
        for (long long nxt : adj[node]) {
            if (!seen[nxt]) {
                seen[nxt] = true;
                stack.push_back(nxt);
            }
        }
    }
    return false;
}

int main() {
    cout << boolalpha << validPath(3, vector<vector<long long>>{vector<long long>{0, 1}, vector<long long>{1, 2}, vector<long long>{2, 0}}, 0, 2) << endl;
    return 0;
}
