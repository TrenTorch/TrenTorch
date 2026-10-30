#include <bits/stdc++.h>
using namespace std;

// O(2^n * n^2) time, O(2^n * n) space
long long tsp(vector<vector<long long>> dist) {
    int n = dist.size();
    if (n <= 1) return 0;
    const long long INF = LLONG_MAX / 4;
    int full = (1 << n) - 1;
    vector<vector<long long>> best(1 << n, vector<long long>(n, INF));
    best[1][0] = 0;
    for (int mask = 1; mask < (1 << n); ++mask) {
        if (!(mask & 1)) continue;
        for (int last = 0; last < n; ++last) {
            long long cost = best[mask][last];
            if (cost == INF) continue;
            for (int nxt = 0; nxt < n; ++nxt) {
                if (!((mask >> nxt) & 1)) {
                    int nm = mask | (1 << nxt);
                    long long value = cost + dist[last][nxt];
                    if (value < best[nm][nxt]) best[nm][nxt] = value;
                }
            }
        }
    }
    long long answer = INF;
    for (int last = 1; last < n; ++last) {
        answer = min(answer, best[full][last] + dist[last][0]);
    }
    return answer;
}

int main() {
    cout << tsp(vector<vector<long long>>{vector<long long>{0, 10, 15, 20}, vector<long long>{10, 0, 35, 25}, vector<long long>{15, 35, 0, 30}, vector<long long>{20, 25, 30, 0}}) << endl;
    return 0;
}
