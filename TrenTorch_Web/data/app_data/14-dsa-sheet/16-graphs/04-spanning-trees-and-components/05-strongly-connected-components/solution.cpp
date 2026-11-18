#include <bits/stdc++.h>
using namespace std;

// O(V + E) time, O(V + E) space (Kosaraju, iterative)
long long countScc(long long n, vector<vector<long long>> edges) {
    int N = n;
    vector<vector<int>> adj(N), rev(N);
    for (auto& e : edges) {
        int a = e[0], b = e[1];
        adj[a].push_back(b);
        rev[b].push_back(a);
    }
    vector<bool> seen(N, false);
    vector<int> order;
    for (int start = 0; start < N; start++) {
        if (seen[start]) continue;
        seen[start] = true;
        vector<pair<int, int>> stk = {{start, 0}};
        while (!stk.empty()) {
            auto [node, i] = stk.back();
            stk.pop_back();
            if (i < (int)adj[node].size()) {
                stk.push_back({node, i + 1});
                int nxt = adj[node][i];
                if (!seen[nxt]) {
                    seen[nxt] = true;
                    stk.push_back({nxt, 0});
                }
            } else {
                order.push_back(node);
            }
        }
    }
    seen.assign(N, false);
    long long count = 0;
    for (int oi = (int)order.size() - 1; oi >= 0; oi--) {
        int start = order[oi];
        if (seen[start]) continue;
        count++;
        seen[start] = true;
        vector<int> stk = {start};
        while (!stk.empty()) {
            int node = stk.back();
            stk.pop_back();
            for (int nxt : rev[node]) {
                if (!seen[nxt]) {
                    seen[nxt] = true;
                    stk.push_back(nxt);
                }
            }
        }
    }
    return count;
}

int main() {
    cout << countScc(5, vector<vector<long long>>{vector<long long>{0, 1}, vector<long long>{1, 2}, vector<long long>{2, 0}, vector<long long>{1, 3}, vector<long long>{3, 4}}) << endl;
    return 0;
}
