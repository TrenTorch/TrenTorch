#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space (stack depth follows bracket nesting)
long long calculateBrackets(string s) {
    vector<pair<long long, long long>> stk;
    long long result = 0, num = 0, sign = 1;
    for (char ch : s) {
        if (isdigit((unsigned char)ch)) {
            num = num * 10 + (ch - '0');
        } else if (ch == '+' || ch == '-') {
            result += sign * num;
            num = 0;
            sign = (ch == '+') ? 1 : -1;
        } else if (ch == '(') {
            stk.push_back({result, sign});
            result = 0;
            sign = 1;
        } else if (ch == ')') {
            result += sign * num;
            num = 0;
            long long savedResult = stk.back().first;
            long long savedSign = stk.back().second;
            stk.pop_back();
            result = savedResult + savedSign * result;
        }
    }
    return result + sign * num;
}

int main() {
    cout << calculateBrackets("(1+(4+5+2)-3)+(6+8)") << endl;
    return 0;
}
