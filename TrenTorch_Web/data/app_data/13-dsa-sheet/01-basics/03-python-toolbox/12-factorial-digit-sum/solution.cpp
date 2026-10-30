#include <bits/stdc++.h>
using namespace std;

// O(n * D) time where D = number of base-1e9 limbs of n! (about 3,900 for n = 10000), O(D) space
long long factorialDigitSum(long long n) {
    const long long BASE = 1000000000LL;
    vector<long long> limbs = {1};  // little-endian base 1e9, value 1
    for (long long m = 2; m <= n; m++) {
        long long carry = 0;
        for (auto& limb : limbs) {
            long long cur = limb * m + carry;
            limb = cur % BASE;
            carry = cur / BASE;
        }
        while (carry > 0) {
            limbs.push_back(carry % BASE);
            carry /= BASE;
        }
    }
    long long sum = 0;
    for (long long limb : limbs) {
        while (limb > 0) {
            sum += limb % 10;
            limb /= 10;
        }
    }
    return sum;
}

int main() {
    cout << factorialDigitSum(10) << endl;
    return 0;
}
