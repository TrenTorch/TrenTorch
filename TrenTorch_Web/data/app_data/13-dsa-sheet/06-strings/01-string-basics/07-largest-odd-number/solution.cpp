#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space for the returned string
string largestOddNumber(string num) {
    for (long long i = (long long)num.size() - 1; i >= 0; i--) {
        if ((num[i] - '0') % 2 == 1) {
            return num.substr(0, (size_t)i + 1);
        }
    }
    return "";
}

int main() {
    cout << largestOddNumber("52") << endl;
    return 0;
}
