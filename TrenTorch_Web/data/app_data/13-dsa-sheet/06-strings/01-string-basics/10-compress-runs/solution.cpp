#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
string compressRuns(string s) {
    string out;
    size_t i = 0;
    while (i < s.size()) {
        size_t j = i;
        while (j < s.size() && s[j] == s[i]) {
            j++;
        }
        size_t n = j - i;
        out += s[i];
        if (n > 1) {
            out += to_string(n);
        }
        i = j;
    }
    return out;
}

int main() {
    cout << compressRuns("aabcccccaaa") << endl;
    return 0;
}
