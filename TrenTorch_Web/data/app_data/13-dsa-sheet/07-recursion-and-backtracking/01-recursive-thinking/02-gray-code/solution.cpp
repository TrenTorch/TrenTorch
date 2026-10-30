#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(2^n) time, O(2^n) space
vector<long long> grayCode(long long n) {
    vector<long long> out;
    out.reserve(1LL << n);
    for (long long i = 0; i < (1LL << n); i++) out.push_back(i ^ (i >> 1));
    return out;
}

int main() {
    cout << grayCode(2) << endl;
    return 0;
}
