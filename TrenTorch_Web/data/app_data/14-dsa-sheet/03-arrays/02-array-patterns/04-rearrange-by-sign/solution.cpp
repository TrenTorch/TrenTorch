#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space
vector<long long> rearrangeBySign(vector<long long> nums) {
    vector<long long> pos, neg;
    for (long long x : nums) {
        if (x >= 0) pos.push_back(x);
        else neg.push_back(x);
    }
    vector<long long> out;
    size_t m = max(pos.size(), neg.size());
    for (size_t i = 0; i < m; i++) {
        if (i < pos.size()) out.push_back(pos[i]);
        if (i < neg.size()) out.push_back(neg[i]);
    }
    return out;
}

int main() {
    cout << rearrangeBySign(vector<long long>{3, 1, -2, -5, 2, -4}) << endl;
    return 0;
}
