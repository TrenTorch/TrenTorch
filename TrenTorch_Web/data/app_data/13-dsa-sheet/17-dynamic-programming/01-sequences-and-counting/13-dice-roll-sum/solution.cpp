#include <bits/stdc++.h>
using namespace std;

// O(dice * target) time, O(target) space
long long diceWays(long long dice, long long faces, long long target) {
    const long long mod = 1000000007LL;
    if (target < 0) return 0;
    vector<long long> row(target + 1, 0);
    row[0] = 1;
    for (long long d = 0; d < dice; d++) {
        vector<long long> prefix(target + 2, 0);
        for (long long t = 0; t <= target; t++) {
            prefix[t + 1] = (prefix[t] + row[t]) % mod;
        }
        vector<long long> nxt(target + 1, 0);
        for (long long t = 1; t <= target; t++) {
            long long diff = prefix[t] - prefix[max(0LL, t - faces)];
            nxt[t] = ((diff % mod) + mod) % mod;
        }
        row = nxt;
    }
    return row[target];
}

int main() {
    cout << diceWays(2, 6, 7) << endl;
    return 0;
}
