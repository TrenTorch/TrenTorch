#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space (alphabet of at most 256 characters)
string removeDuplicateLetters(string s) {
    long long n = s.size();
    vector<long long> last(256, -1);
    for (long long i = 0; i < n; i++) {
        last[(unsigned char)s[i]] = i;
    }
    string stack;
    vector<bool> inStack(256, false);
    for (long long i = 0; i < n; i++) {
        unsigned char ch = s[i];
        if (inStack[ch]) continue;
        while (!stack.empty()) {
            unsigned char top = stack.back();
            if (!(top > ch && last[top] > i)) break;
            inStack[top] = false;
            stack.pop_back();
        }
        stack.push_back((char)ch);
        inStack[ch] = true;
    }
    return stack;
}

int main() {
    cout << removeDuplicateLetters("bcabc") << endl;
    return 0;
}
