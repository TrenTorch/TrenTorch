#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long stockBestProfit(vector<long long> prices) {
    if (prices.empty()) return 0;
    long long best = 0, lowest = prices[0];
    for (size_t i = 1; i < prices.size(); i++) {
        best = max(best, prices[i] - lowest);
        lowest = min(lowest, prices[i]);
    }
    return best;
}

int main() {
    cout << stockBestProfit(vector<long long>{7, 1, 5, 3, 6, 4}) << endl;
    return 0;
}
