#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(1) space (fixed 256-entry table of last occurrences)
vector<long long> partitionLabels(string s) {
    long long n = s.size();
    vector<long long> last(256, -1);
    for (long long i = 0; i < n; i++) {
        last[(unsigned char)s[i]] = i;
    }
    vector<long long> sizes;
    long long start = 0;
    long long end = 0;
    for (long long i = 0; i < n; i++) {
        end = max(end, last[(unsigned char)s[i]]);
        if (i == end) {
            sizes.push_back(end - start + 1);
            start = i + 1;
        }
    }
    return sizes;
}

int main() {
    cout << partitionLabels("ababcbacadefegdehijhklij") << endl;
    return 0;
}
