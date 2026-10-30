#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n^2) precomputation plus O(n * 2^n) time for the search, O(n^2) space for the table
vector<vector<string>> palindromePartitions(string s) {
    int n = s.size();
    vector<vector<bool>> pal(n, vector<bool>(n, false));
    for (int length = 1; length <= n; length++) {
        for (int i = 0; i + length <= n; i++) {
            int j = i + length - 1;
            pal[i][j] = s[i] == s[j] && (length <= 2 || pal[i + 1][j - 1]);
        }
    }
    vector<vector<string>> out;
    vector<string> pieces;
    function<void(int)> go = [&](int start) {
        if (start == n) {
            out.push_back(pieces);
            return;
        }
        for (int j = start; j < n; j++) {
            if (pal[start][j]) {
                pieces.push_back(s.substr(start, j - start + 1));
                go(j + 1);
                pieces.pop_back();
            }
        }
    };
    go(0);
    return out;
}

int main() {
    cout << palindromePartitions("aab") << endl;
    return 0;
}
