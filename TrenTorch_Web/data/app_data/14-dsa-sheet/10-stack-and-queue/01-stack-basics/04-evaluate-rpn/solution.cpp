#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
long long evaluateRpn(vector<string> tokens) {
    vector<long long> st;
    for (const string& token : tokens) {
        if (token == "+" || token == "-" || token == "*" || token == "/") {
            long long b = st.back();
            st.pop_back();
            long long a = st.back();
            st.pop_back();
            if (token == "+") st.push_back(a + b);
            else if (token == "-") st.push_back(a - b);
            else if (token == "*") st.push_back(a * b);
            else st.push_back(a / b);
        } else {
            st.push_back(stoll(token));
        }
    }
    return st[0];
}

int main() {
    cout << evaluateRpn(vector<string>{"2", "1", "+", "3", "*"}) << endl;
    return 0;
}
