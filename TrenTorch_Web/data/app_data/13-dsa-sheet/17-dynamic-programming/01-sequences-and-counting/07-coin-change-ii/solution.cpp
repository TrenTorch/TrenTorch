#include <bits/stdc++.h>
using namespace std;

// O(amount * len(coins)) time, O(amount) space
long long countChange(long long amount, vector<long long> coins) {
    const long long mod = 1000000007LL;
    if (amount < 0) return 0;
    vector<long long> ways(amount + 1, 0);
    ways[0] = 1;
    for (long long c : coins) {
        for (long long a = c; a <= amount; a++) {
            ways[a] = (ways[a] + ways[a - c]) % mod;
        }
    }
    return ways[amount];
}

int main() {
    cout << countChange(5, vector<long long>{1, 2, 5}) << endl;
    return 0;
}
