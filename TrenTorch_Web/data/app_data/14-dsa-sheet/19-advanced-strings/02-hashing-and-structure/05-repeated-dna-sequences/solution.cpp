#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space (hash set of 10-letter windows, then sort)
vector<string> repeatedDna(string s) {
    unordered_set<string> seen, repeated;
    for (size_t i = 0; i + 10 <= s.size(); i++) {
        string part = s.substr(i, 10);
        if (seen.count(part)) repeated.insert(part);
        else seen.insert(part);
    }
    vector<string> out(repeated.begin(), repeated.end());
    sort(out.begin(), out.end());
    return out;
}

int main() {
    cout << repeatedDna("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT") << endl;
    return 0;
}
