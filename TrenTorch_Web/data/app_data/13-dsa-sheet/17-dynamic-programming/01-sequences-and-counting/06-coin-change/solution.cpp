#include <bits/stdc++.h>
using namespace std;

// O(amount * len(coins)) time, O(amount) space
long long coinChange(vector<long long> coins, long long amount) {
    const long long INF = LLONG_MAX / 4;
    if (amount < 0) return -1;
    vector<long long> best(amount + 1, INF);
    best[0] = 0;
    for (long long a = 1; a <= amount; a++) {
        for (long long c : coins) {
            if (c <= a && best[a - c] + 1 < best[a]) {
                best[a] = best[a - c] + 1;
            }
        }
    }
    return best[amount] != INF ? best[amount] : -1;
}

int main() {
    cout << coinChange(vector<long long>{1, 2, 5}, 11) << endl;
    return 0;
}
