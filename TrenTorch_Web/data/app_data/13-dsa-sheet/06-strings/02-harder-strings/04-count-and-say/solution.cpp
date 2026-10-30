#include <bits/stdc++.h>
using namespace std;

// O(L * n) time, where L is the length of term n; O(L) space
string countAndSay(long long n) {
    string term = "1";
    for (long long step = 0; step < n - 1; step++) {
        string next;
        size_t i = 0;
        while (i < term.size()) {
            size_t j = i;
            while (j < term.size() && term[j] == term[i]) j++;
            next += to_string(j - i);
            next += term[i];
            i = j;
        }
        term = next;
    }
    return term;
}

int main() {
    cout << countAndSay(4) << endl;
    return 0;
}
