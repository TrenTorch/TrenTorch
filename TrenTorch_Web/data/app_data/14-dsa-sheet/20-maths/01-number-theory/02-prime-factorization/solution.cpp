#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(sqrt(n)) time, O(log n) space
vector<vector<long long>> primeFactors(long long n) {
    vector<vector<long long>> out;
    long long d = 2;
    while (d * d <= n) {
        if (n % d == 0) {
            long long e = 0;
            while (n % d == 0) {
                n /= d;
                e++;
            }
            out.push_back({d, e});
        }
        d += (d == 2) ? 1 : 2;
    }
    if (n > 1) out.push_back({n, 1});
    return out;
}

int main() {
    cout << primeFactors(360) << endl;
    return 0;
}
