#include <bits/stdc++.h>
using namespace std;

// KMP: O(n + m) time, O(m) space
long long countOverlapping(string text, string pattern) {
    int m = pattern.size();
    vector<int> fail(m, 0);
    int k = 0;
    for (int i = 1; i < m; i++) {
        while (k > 0 && pattern[i] != pattern[k]) k = fail[k - 1];
        if (pattern[i] == pattern[k]) k++;
        fail[i] = k;
    }
    long long count = 0;
    k = 0;
    for (char ch : text) {
        while (k > 0 && ch != pattern[k]) k = fail[k - 1];
        if (ch == pattern[k]) k++;
        if (k == m) {
            count++;
            k = fail[k - 1];
        }
    }
    return count;
}

int main() {
    cout << countOverlapping("aaaa", "aa") << endl;
    return 0;
}
