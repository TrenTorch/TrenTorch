#include <bits/stdc++.h>
using namespace std;

// O(d) time, O(d) space where d is the number of digits of n
long long monotoneIncreasingDigits(long long n) {
    string digits = to_string(n);
    size_t mark = digits.size();
    for (size_t i = digits.size() - 1; i > 0; i--) {
        if (digits[i - 1] > digits[i]) {
            digits[i - 1]--;
            mark = i;
        }
    }
    for (size_t i = mark; i < digits.size(); i++) digits[i] = '9';
    return stoll(digits);
}

int main() {
    cout << monotoneIncreasingDigits(332) << endl;
    return 0;
}
