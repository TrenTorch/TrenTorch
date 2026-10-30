#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(1) space
vector<long long> twoSingleNumbers(vector<long long> nums) {
    long long xorAll = 0;
    for (long long x : nums) xorAll ^= x;
    long long low = xorAll & -xorAll;
    long long a = 0, b = 0;
    for (long long x : nums) {
        if (x & low) a ^= x;
        else b ^= x;
    }
    return {min(a, b), max(a, b)};
}

int main() {
    cout << twoSingleNumbers(vector<long long>{1, 2, 1, 3, 2, 5}) << endl;
    return 0;
}
