#include <bits/stdc++.h>
using namespace std;

// O(n^3) time worst case (Knuth-style bounded search), O(n^2) space
long long minCostCut(long long length, vector<long long> cuts) {
    sort(cuts.begin(), cuts.end());
    vector<long long> points;
    points.push_back(0);
    for (long long c : cuts) points.push_back(c);
    points.push_back(length);
    int n = points.size();
    vector<vector<long long>> dp(n, vector<long long>(n, 0));
    vector<vector<int>> bestCut(n, vector<int>(n, 0));
    for (int i = 0; i + 1 < n; i++) bestCut[i][i + 1] = i + 1;
    for (int span = 2; span < n; span++) {
        for (int i = 0; i + span < n; i++) {
            int j = i + span;
            int low = max(i + 1, bestCut[i][j - 1]);
            int high = min(j - 1, bestCut[i + 1][j]);
            long long best = LLONG_MAX;
            for (int k = low; k <= high; k++) {
                long long value = dp[i][k] + dp[k][j];
                if (value < best) {
                    best = value;
                    bestCut[i][j] = k;
                }
            }
            dp[i][j] = best + points[j] - points[i];
        }
    }
    return dp[0][n - 1];
}

int main() {
    cout << minCostCut(7, vector<long long>{1, 3, 4, 5}) << endl;
    return 0;
}
