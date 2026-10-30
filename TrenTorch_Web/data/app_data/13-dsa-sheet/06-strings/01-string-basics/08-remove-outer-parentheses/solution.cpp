#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
string removeOuterParentheses(string s) {
    string out;
    long long depth = 0;
    for (char ch : s) {
        if (ch == '(') {
            if (depth > 0) {
                out += ch;
            }
            depth++;
        } else {
            depth--;
            if (depth > 0) {
                out += ch;
            }
        }
    }
    return out;
}

int main() {
    cout << removeOuterParentheses("(()())(())") << endl;
    return 0;
}
