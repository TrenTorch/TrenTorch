#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space (two fixed 256-entry mapping tables)
bool isomorphicStrings(string s, string t) {
    if (s.size() != t.size()) return false;
    int forward[256], backward[256];
    fill(forward, forward + 256, -1);
    fill(backward, backward + 256, -1);
    for (size_t i = 0; i < s.size(); i++) {
        unsigned char a = s[i], b = t[i];
        if (forward[a] == -1) forward[a] = b;
        else if (forward[a] != b) return false;
        if (backward[b] == -1) backward[b] = a;
        else if (backward[b] != a) return false;
    }
    return true;
}

int main() {
    cout << boolalpha << isomorphicStrings("egg", "add") << endl;
    return 0;
}
