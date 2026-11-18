#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space (fixed 256-entry table)
long long firstUniqueCharacter(string s) {
    int counts[256] = {0};
    for (unsigned char c : s) counts[c]++;
    for (size_t i = 0; i < s.size(); i++) {
        if (counts[(unsigned char)s[i]] == 1) return (long long)i;
    }
    return -1;
}

int main() {
    cout << firstUniqueCharacter("leetcode") << endl;
    return 0;
}
