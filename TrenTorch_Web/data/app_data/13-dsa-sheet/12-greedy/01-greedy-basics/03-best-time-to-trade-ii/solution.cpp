#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long maxProfitMany(vector<long long> prices) {
    long long total = 0;
    for (size_t i = 1; i < prices.size(); i++) {
        total += max(0LL, prices[i] - prices[i - 1]);
    }
    return total;
}

int main() {
    cout << maxProfitMany(vector<long long>{7, 1, 5, 3, 6, 4}) << endl;
    return 0;
}
