#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
string removeAdjacentDuplicates(string s) {
    string st;
    for (char ch : s) {
        if (!st.empty() && st.back() == ch) st.pop_back();
        else st.push_back(ch);
    }
    return st;
}

int main() {
    cout << removeAdjacentDuplicates("abbaca") << endl;
    return 0;
}
