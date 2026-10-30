#include <bits/stdc++.h>
using namespace std;

// O(n^3) time, O(n^2) space
long long maxCoins(vector<long long> nums) {
    vector<long long> a;
    a.push_back(1);
    for (long long x : nums) a.push_back(x);
    a.push_back(1);
    int n = a.size();
    vector<vector<long long>> dp(n, vector<long long>(n, 0));
    for (int length = 2; length < n; ++length) {
        for (int i = 0; i + length < n; ++i) {
            int j = i + length;
            long long best = 0;
            for (int k = i + 1; k < j; ++k) {
                long long value = dp[i][k] + dp[k][j] + a[i] * a[k] * a[j];
                if (value > best) best = value;
            }
            dp[i][j] = best;
        }
    }
    return dp[0][n - 1];
}

int main() {
    cout << maxCoins(vector<long long>{3, 1, 5, 8}) << endl;
    return 0;
}
