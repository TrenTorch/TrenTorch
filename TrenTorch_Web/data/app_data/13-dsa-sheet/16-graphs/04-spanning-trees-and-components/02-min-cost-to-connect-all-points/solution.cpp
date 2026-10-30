#include <bits/stdc++.h>
using namespace std;

// O(n^2) time, O(n) space
long long minCostConnectPoints(vector<vector<long long>> points) {
    int n = points.size();
    if (n == 0) return 0;
    const long long INF = LLONG_MAX;
    vector<long long> best(n, INF);
    best[0] = 0;
    vector<bool> used(n, false);
    long long total = 0;
    for (int it = 0; it < n; it++) {
        int u = -1;
        for (int v = 0; v < n; v++) {
            if (!used[v] && (u == -1 || best[v] < best[u])) u = v;
        }
        used[u] = true;
        total += best[u];
        long long ux = points[u][0], uy = points[u][1];
        for (int v = 0; v < n; v++) {
            if (!used[v]) {
                long long dist = llabs(points[v][0] - ux) + llabs(points[v][1] - uy);
                if (dist < best[v]) best[v] = dist;
            }
        }
    }
    return total;
}

int main() {
    cout << minCostConnectPoints(vector<vector<long long>>{vector<long long>{0, 0}, vector<long long>{2, 2}, vector<long long>{3, 10}, vector<long long>{5, 2}, vector<long long>{7, 0}}) << endl;
    return 0;
}
