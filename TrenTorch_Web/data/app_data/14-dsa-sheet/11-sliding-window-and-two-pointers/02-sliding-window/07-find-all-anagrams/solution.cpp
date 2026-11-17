#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(1) extra space (fixed 26-entry tables; output excluded)
vector<long long> findAnagrams(string s, string p) {
    long long m = p.size();
    long long n = s.size();
    if (m == 0 || m > n) {
        return {};
    }
    vector<long long> need(26, 0), window(26, 0), out;
    for (char ch : p) {
        need[ch - 'a']++;
    }
    for (long long i = 0; i < n; i++) {
        window[s[i] - 'a']++;
        if (i >= m) {
            window[s[i - m] - 'a']--;
        }
        if (i >= m - 1 && window == need) {
            out.push_back(i - m + 1);
        }
    }
    return out;
}

int main() {
    cout << findAnagrams("cbaebabacd", "abc") << endl;
    return 0;
}
