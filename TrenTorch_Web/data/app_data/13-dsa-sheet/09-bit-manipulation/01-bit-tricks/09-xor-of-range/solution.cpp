#include <bits/stdc++.h>
using namespace std;

// O(1) time, O(1) space
long long xorOfRange(long long left, long long right) {
    auto prefix = [](long long n) -> long long {
        if (n < 0) return 0;
        long long r = n % 4;
        if (r == 0) return n;
        if (r == 1) return 1;
        if (r == 2) return n + 1;
        return 0;
    };
    return prefix(right) ^ prefix(left - 1);
}

int main() {
    cout << xorOfRange(3, 9) << endl;
    return 0;
}
