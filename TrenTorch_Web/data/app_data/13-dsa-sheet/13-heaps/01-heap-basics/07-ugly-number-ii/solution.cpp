#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
long long nthUglyNumber(long long n) {
    vector<long long> ugly = {1};
    size_t i2 = 0, i3 = 0, i5 = 0;
    while ((long long)ugly.size() < n) {
        long long nxt = min({ugly[i2] * 2, ugly[i3] * 3, ugly[i5] * 5});
        ugly.push_back(nxt);
        if (nxt == ugly[i2] * 2) i2++;
        if (nxt == ugly[i3] * 3) i3++;
        if (nxt == ugly[i5] * 5) i5++;
    }
    return ugly[n - 1];
}

int main() {
    cout << nthUglyNumber(10) << endl;
    return 0;
}
