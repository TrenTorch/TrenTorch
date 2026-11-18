#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space
vector<long long> zFunction(string s) {
    int n = s.size();
    vector<long long> z(n, 0);
    long long left = 0, right = 0;
    for (long long i = 1; i < n; i++) {
        if (i < right) z[i] = min<long long>(right - i, z[i - left]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] > right) {
            left = i;
            right = i + z[i];
        }
    }
    return z;
}

int main() {
    cout << zFunction("aabxaab") << endl;
    return 0;
}
