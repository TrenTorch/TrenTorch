#include <bits/stdc++.h>
using namespace std;

// O(n * m) time, O(min(n, m)) space
long long editDistance(string a, string b) {
    if (b.size() > a.size()) swap(a, b);
    vector<long long> prev(b.size() + 1, 0);
    for (size_t j = 0; j <= b.size(); j++) prev[j] = (long long)j;
    for (size_t i = 1; i <= a.size(); i++) {
        vector<long long> cur(b.size() + 1, 0);
        cur[0] = (long long)i;
        for (size_t j = 1; j <= b.size(); j++) {
            if (a[i - 1] == b[j - 1]) {
                cur[j] = prev[j - 1];
            } else {
                cur[j] = 1 + min({prev[j - 1], prev[j], cur[j - 1]});
            }
        }
        prev = cur;
    }
    return prev[b.size()];
}

int main() {
    cout << editDistance("horse", "ros") << endl;
    return 0;
}
