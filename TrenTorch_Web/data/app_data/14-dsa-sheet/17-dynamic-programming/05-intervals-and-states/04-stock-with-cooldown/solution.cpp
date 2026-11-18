#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long maxProfitCooldown(vector<long long> prices) {
    const long long NEG = LLONG_MIN / 4;
    long long hold = NEG, sold = 0, rest = 0;
    for (long long price : prices) {
        long long newHold = max(hold, rest - price);
        long long newSold = hold + price;
        long long newRest = max(rest, sold);
        hold = newHold;
        sold = newSold;
        rest = newRest;
    }
    return max(sold, rest);
}

int main() {
    cout << maxProfitCooldown(vector<long long>{1, 2, 3, 0, 2}) << endl;
    return 0;
}
