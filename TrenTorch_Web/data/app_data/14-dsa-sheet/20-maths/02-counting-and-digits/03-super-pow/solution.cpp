#include <bits/stdc++.h>
using namespace std;

// O(len(b) * log 10) time, O(1) space
long long superPow(long long a, vector<long long> b) {
    const long long M = 1337;
    auto pw = [&](long long base, long long e) -> long long {
        long long r = 1;
        base %= M;
        while (e > 0) {
            if (e & 1) r = r * base % M;
            base = base * base % M;
            e >>= 1;
        }
        return r;
    };
    long long result = 1;
    for (long long digit : b) {
        result = pw(result, 10) * pw(a, digit) % M;
    }
    return result;
}

int main() {
    cout << superPow(2, vector<long long>{1, 0}) << endl;
    return 0;
}
