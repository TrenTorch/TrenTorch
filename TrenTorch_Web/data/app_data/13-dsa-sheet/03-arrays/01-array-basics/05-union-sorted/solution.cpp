#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n + m) time, O(n + m) space for the result
vector<long long> unionSorted(vector<long long> a, vector<long long> b) {
    vector<long long> out;
    size_t i = 0, j = 0;
    while (i < a.size() || j < b.size()) {
        long long x;
        if (j == b.size() || (i < a.size() && a[i] <= b[j])) {
            x = a[i++];
        } else {
            x = b[j++];
        }
        if (out.empty() || out.back() != x) out.push_back(x);
    }
    return out;
}

int main() {
    cout << unionSorted(vector<long long>{1, 2, 2, 4}, vector<long long>{2, 3, 4, 5}) << endl;
    return 0;
}
