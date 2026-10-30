#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long myAtoi(string s) {
    long long i = 0, n = s.size();
    while (i < n && s[i] == ' ') i++;
    long long sign = 1;
    if (i < n && (s[i] == '+' || s[i] == '-')) {
        sign = (s[i] == '-') ? -1 : 1;
        i++;
    }
    long long value = 0;
    while (i < n && s[i] >= '0' && s[i] <= '9') {
        value = value * 10 + (s[i] - '0');
        i++;
        if (value > (1LL << 31)) break;
    }
    value *= sign;
    return max(-(1LL << 31), min((1LL << 31) - 1, value));
}

int main() {
    cout << myAtoi("42") << endl;
    return 0;
}
