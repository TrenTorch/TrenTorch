#include <bits/stdc++.h>
using namespace std;

static bool isPalindromeRange(const string& s, int i, int j) {
    while (i < j) {
        if (s[i] != s[j]) return false;
        i++;
        j--;
    }
    return true;
}

// O(n) time, O(1) space
bool validPalindromeIi(string s) {
    int i = 0, j = (int)s.size() - 1;
    while (i < j) {
        if (s[i] != s[j]) return isPalindromeRange(s, i + 1, j) || isPalindromeRange(s, i, j - 1);
        i++;
        j--;
    }
    return true;
}

int main() {
    cout << boolalpha << validPalindromeIi("aba") << endl;
    return 0;
}
