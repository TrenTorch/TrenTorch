#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
bool validBrackets(string s) {
    stack<char> st;
    for (char ch : s) {
        if (ch == ')' || ch == ']' || ch == '}') {
            char open = (ch == ')') ? '(' : (ch == ']') ? '[' : '{';
            if (st.empty() || st.top() != open) return false;
            st.pop();
        } else {
            st.push(ch);
        }
    }
    return st.empty();
}

int main() {
    cout << boolalpha << validBrackets("()[]{}") << endl;
    return 0;
}
