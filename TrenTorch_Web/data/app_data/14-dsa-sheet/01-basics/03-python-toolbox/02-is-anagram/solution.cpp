#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space (fixed 256-entry count table)
bool isAnagram(string a, string b) {
    if (a.size() != b.size()) return false;
    vector<long long> count(256, 0);
    for (size_t i = 0; i < a.size(); i++) {
        count[(unsigned char)a[i]]++;
        count[(unsigned char)b[i]]--;
    }
    for (long long c : count) {
        if (c != 0) return false;
    }
    return true;
}

int main() {
    cout << boolalpha << isAnagram("listen", "silent") << endl;
    return 0;
}
