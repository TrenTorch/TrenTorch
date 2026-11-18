#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long maxNestingDepth(string s) {
    long long depth = 0, best = 0;
    for (char ch : s) {
        if (ch == '(') {
            depth++;
            best = max(best, depth);
        } else if (ch == ')') {
            depth--;
        }
    }
    return best;
}

int main() {
    cout << maxNestingDepth("(1+(2*3)+((8)/4))+1") << endl;
    return 0;
}
