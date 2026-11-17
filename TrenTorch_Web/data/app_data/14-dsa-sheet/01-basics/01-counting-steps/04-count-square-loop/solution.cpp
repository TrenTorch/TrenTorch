#include <bits/stdc++.h>
using namespace std;

// O(1) time, O(1) space
long long countSquareLoop(long long n) {
    long long r = (long long)sqrtl((long double)n);
    while (r * r > n) r--;
    while ((r + 1) * (r + 1) <= n) r++;
    return r;
}

int main() {
    cout << countSquareLoop(10) << endl;
    return 0;
}
