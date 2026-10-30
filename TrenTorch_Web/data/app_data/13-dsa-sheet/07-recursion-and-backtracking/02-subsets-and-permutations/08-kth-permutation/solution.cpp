#include <bits/stdc++.h>
using namespace std;

// O(n^2) time, O(n) space
string kthPermutation(long long n, long long k) {
    vector<long long> remaining;
    for (long long i = 1; i <= n; i++) remaining.push_back(i);
    vector<long long> fact(n + 1, 1LL);
    for (long long i = 1; i <= n; i++) fact[i] = fact[i - 1] * i;
    k -= 1;
    string out;
    for (long long size = n - 1; size >= 0; size--) {
        long long index = k / fact[size];
        k %= fact[size];
        out += to_string(remaining[index]);
        remaining.erase(remaining.begin() + index);
    }
    return out;
}

int main() {
    cout << kthPermutation(3, 3) << endl;
    return 0;
}
