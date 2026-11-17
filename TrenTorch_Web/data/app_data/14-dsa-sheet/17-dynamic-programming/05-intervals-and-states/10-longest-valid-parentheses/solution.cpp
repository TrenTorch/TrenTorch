#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long longestValidParentheses(string s) {
    long long best = 0;
    int n = s.size();
    for (int pass = 0; pass < 2; pass++) {
        char opener = pass == 0 ? '(' : ')';
        long long left = 0, right = 0;
        for (int idx = 0; idx < n; idx++) {
            char ch = pass == 0 ? s[idx] : s[n - 1 - idx];
            if (ch == opener) left++;
            else right++;
            if (left == right) best = max(best, 2 * left);
            else if (right > left) left = right = 0;
        }
    }
    return best;
}

int main() {
    cout << longestValidParentheses(")()())") << endl;
    return 0;
}
