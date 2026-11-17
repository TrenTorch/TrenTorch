#include <bits/stdc++.h>
using namespace std;

// O(n + m) time, O(n + m) space (m = number of edges)
bool hasCycleDirected(long long n, vector<vector<long long>> edges) {
    vector<vector<long long>> adj(n);
    for (const auto& e : edges) adj[e[0]].push_back(e[1]);
    vector<int> state(n, 0);
    for (long long start = 0; start < n; start++) {
        if (state[start]) continue;
        state[start] = 1;
        vector<pair<long long, long long>> stack = {{start, 0}};
        while (!stack.empty()) {
            auto [node, i] = stack.back();
            stack.pop_back();
            if (i < (long long)adj[node].size()) {
                stack.push_back({node, i + 1});
                long long nxt = adj[node][i];
                if (state[nxt] == 1) return true;
                if (state[nxt] == 0) {
                    state[nxt] = 1;
                    stack.push_back({nxt, 0});
                }
            } else {
                state[node] = 2;
            }
        }
    }
    return false;
}

int main() {
    cout << boolalpha << hasCycleDirected(3, vector<vector<long long>>{vector<long long>{0, 1}, vector<long long>{1, 2}, vector<long long>{2, 0}}) << endl;
    return 0;
}
