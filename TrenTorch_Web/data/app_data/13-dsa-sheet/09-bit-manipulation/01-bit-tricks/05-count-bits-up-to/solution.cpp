#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space
vector<long long> countBitsUpTo(long long n) {
    vector<long long> bits(n + 1, 0);
    for (long long i = 1; i <= n; i++) {
        bits[i] = bits[i >> 1] + (i & 1);
    }
    return bits;
}

int main() {
    cout << countBitsUpTo(5) << endl;
    return 0;
}
