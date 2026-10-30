#include <bits/stdc++.h>
using namespace std;

// O(n^3) time, O(n^2) space
long long matrixChainCost(vector<long long> dims) {
    int n = dims.size();
    if (n < 3) return 0;
    const long long INF = LLONG_MAX / 4;
    vector<vector<long long>> dp(n, vector<long long>(n, 0));
    for (int length = 2; length < n; ++length) {
        for (int i = 0; i + length < n; ++i) {
            int j = i + length;
            long long best = INF;
            for (int k = i + 1; k < j; ++k) {
                long long value = dp[i][k] + dp[k][j] + dims[i] * dims[k] * dims[j];
                if (value < best) best = value;
            }
            dp[i][j] = best;
        }
    }
    return dp[0][n - 1];
}

int main() {
    cout << matrixChainCost(vector<long long>{10, 30, 5, 60}) << endl;
    return 0;
}
