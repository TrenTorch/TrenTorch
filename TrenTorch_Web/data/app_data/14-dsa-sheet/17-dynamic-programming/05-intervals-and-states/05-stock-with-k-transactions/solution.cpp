#include <bits/stdc++.h>
using namespace std;

// O(n * k) time, O(k) space (O(n) when k >= n / 2)
long long maxProfitK(long long k, vector<long long> prices) {
    long long n = prices.size();
    if (k == 0 || n < 2) return 0;
    if (k >= n / 2) {
        long long total = 0;
        for (long long i = 1; i < n; ++i) total += max(0LL, prices[i] - prices[i - 1]);
        return total;
    }
    const long long NEG = LLONG_MIN / 4;
    int K = k;
    vector<long long> hold(K + 1, NEG), freeCash(K + 1, 0);
    for (long long p : prices) {
        for (int t = 1; t <= K; ++t) {
            hold[t] = max(hold[t], freeCash[t - 1] - p);
            freeCash[t] = max(freeCash[t], hold[t] + p);
        }
    }
    return freeCash[K];
}

int main() {
    cout << maxProfitK(2, vector<long long>{3, 2, 6, 5, 0, 3}) << endl;
    return 0;
}
