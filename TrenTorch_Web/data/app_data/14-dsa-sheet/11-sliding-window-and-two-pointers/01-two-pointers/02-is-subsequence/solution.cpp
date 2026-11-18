#include <bits/stdc++.h>
using namespace std;

// O(n + m) time, O(1) space
bool isSubsequence(string s, string t) {
    size_t i = 0;
    for (char ch : t) {
        if (i < s.size() && s[i] == ch) i++;
    }
    return i == s.size();
}

int main() {
    cout << boolalpha << isSubsequence("ace", "abcde") << endl;
    return 0;
}
