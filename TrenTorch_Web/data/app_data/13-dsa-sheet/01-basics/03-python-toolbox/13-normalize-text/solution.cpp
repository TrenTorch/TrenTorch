#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
string normalizeText(string s) {
    string out;
    for (char ch : s) {
        char c = (ch >= 'A' && ch <= 'Z') ? (char)(ch - 'A' + 'a') : ch;
        if ((c >= 'a' && c <= 'z') || (c >= '0' && c <= '9')) {
            out.push_back(c);
        } else if (!out.empty() && out.back() != ' ') {
            out.push_back(' ');
        }
    }
    if (!out.empty() && out.back() == ' ') out.pop_back();
    return out;
}

int main() {
    cout << normalizeText("  Hello,   World!! 42 ") << endl;
    return 0;
}
