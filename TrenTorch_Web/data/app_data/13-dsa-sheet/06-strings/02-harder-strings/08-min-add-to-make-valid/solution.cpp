#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long minAddToMakeValid(string s) {
    long long open_count = 0, need = 0;
    for (char ch : s) {
        if (ch == '(') {
            open_count++;
        } else if (open_count) {
            open_count--;
        } else {
            need++;
        }
    }
    return need + open_count;
}

int main() {
    cout << minAddToMakeValid("())") << endl;
    return 0;
}
