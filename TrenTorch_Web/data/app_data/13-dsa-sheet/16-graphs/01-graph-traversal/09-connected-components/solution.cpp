#include <bits/stdc++.h>
using namespace std;

// O(n + m) time, O(n + m) space (m = number of edges)
long long countComponents(long long n, vector<vector<long long>> edges) {
    vector<vector<long long>> adj(n);
    for (const auto& e : edges) {
        adj[e[0]].push_back(e[1]);
        adj[e[1]].push_back(e[0]);
    }
    vector<bool> seen(n, false);
    long long count = 0;
    for (long long start = 0; start < n; start++) {
        if (seen[start]) continue;
        count++;
        seen[start] = true;
        vector<long long> stack = {start};
        while (!stack.empty()) {
            long long node = stack.back();
            stack.pop_back();
            for (long long nxt : adj[node]) {
                if (!seen[nxt]) {
                    seen[nxt] = true;
                    stack.push_back(nxt);
                }
            }
        }
    }
    return count;
}

int main() {
    cout << countComponents(5, vector<vector<long long>>{vector<long long>{0, 1}, vector<long long>{1, 2}, vector<long long>{3, 4}}) << endl;
    return 0;
}
