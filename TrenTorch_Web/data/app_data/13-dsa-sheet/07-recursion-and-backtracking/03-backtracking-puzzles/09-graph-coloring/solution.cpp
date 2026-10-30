#include <bits/stdc++.h>
using namespace std;

// O(colors^n) time worst case, O(n + m) space for the graph
bool canColorGraph(long long n, vector<vector<long long>> edges, long long colors) {
    for (const auto& e : edges) {
        if (e[0] == e[1]) return false;
    }
    vector<vector<long long>> adj(n);
    for (const auto& e : edges) {
        adj[e[0]].push_back(e[1]);
        adj[e[1]].push_back(e[0]);
    }
    vector<long long> color(n, -1);
    function<bool(long long)> go = [&](long long i) -> bool {
        if (i == n) return true;
        for (long long c = 0; c < colors; c++) {
            bool ok = true;
            for (long long j : adj[i]) {
                if (color[j] == c) {
                    ok = false;
                    break;
                }
            }
            if (ok) {
                color[i] = c;
                if (go(i + 1)) return true;
                color[i] = -1;
            }
        }
        return false;
    };
    return go(0);
}

int main() {
    cout << boolalpha << canColorGraph(3, vector<vector<long long>>{vector<long long>{0, 1}, vector<long long>{1, 2}, vector<long long>{0, 2}}, 3) << endl;
    return 0;
}
