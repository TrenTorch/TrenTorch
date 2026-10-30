#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
bool checkValidString(string s) {
    long long lo = 0;
    long long hi = 0;
    for (char ch : s) {
        if (ch == '(') {
            lo++;
            hi++;
        } else if (ch == ')') {
            lo--;
            hi--;
        } else {
            lo--;
            hi++;
        }
        if (hi < 0) return false;
        lo = max(lo, 0LL);
    }
    return lo == 0;
}

int main() {
    cout << boolalpha << checkValidString("(*)") << endl;
    return 0;
}
