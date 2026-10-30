#include <bits/stdc++.h>
using namespace std;

// O(length^2) time, O(length) space
long long rodCutting(vector<long long> prices, long long length) {
    int L = length;
    vector<long long> best(L + 1, 0);
    for (int n = 1; n <= L; ++n) {
        for (int k = 1; k <= n; ++k) {
            if (prices[k - 1] + best[n - k] > best[n]) best[n] = prices[k - 1] + best[n - k];
        }
    }
    return best[L];
}

int main() {
    cout << rodCutting(vector<long long>{1, 5, 8, 9, 10, 17, 17, 20}, 8) << endl;
    return 0;
}
