#include <bits/stdc++.h>
using namespace std;

// O(n + m) time, O(1) space
bool backspaceCompare(string s, string t) {
    auto nextTyped = [](const string& text, int i) -> int {
        int skip = 0;
        while (i >= 0) {
            if (text[i] == '#') {
                skip++;
            } else if (skip) {
                skip--;
            } else {
                return i;
            }
            i--;
        }
        return -1;
    };

    int i = (int)s.size() - 1;
    int j = (int)t.size() - 1;
    while (true) {
        i = nextTyped(s, i);
        j = nextTyped(t, j);
        if (i < 0 && j < 0) return true;
        if (i < 0 || j < 0 || s[i] != t[j]) return false;
        i--;
        j--;
    }
}

int main() {
    cout << boolalpha << backspaceCompare("ab#c", "ad#c") << endl;
    return 0;
}
