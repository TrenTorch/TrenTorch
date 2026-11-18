#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long calculate(string s) {
    long long total = 0, last = 0, num = 0;
    char op = '+';
    s += '+';
    for (char ch : s) {
        if (isdigit((unsigned char)ch)) {
            num = num * 10 + (ch - '0');
        } else if (ch != ' ') {
            if (op == '+') {
                total += last;
                last = num;
            } else if (op == '-') {
                total += last;
                last = -num;
            } else if (op == '*') {
                last *= num;
            } else {
                long long q = llabs(last) / num;
                last = (last >= 0) ? q : -q;
            }
            op = ch;
            num = 0;
        }
    }
    return total + last;
}

int main() {
    cout << calculate("3+2*2") << endl;
    return 0;
}
