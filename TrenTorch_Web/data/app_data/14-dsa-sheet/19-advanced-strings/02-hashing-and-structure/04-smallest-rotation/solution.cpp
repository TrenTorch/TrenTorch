#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space (two-pointer minimal rotation)
string smallestRotation(string s) {
    long long n = s.size();
    if (n == 0) return "";
    string s2 = s + s;
    long long i = 0, j = 1, k = 0;
    while (i < n && j < n && k < n) {
        char a = s2[i + k], b = s2[j + k];
        if (a == b) {
            k++;
            continue;
        }
        if (a > b) i += k + 1;
        else j += k + 1;
        if (i == j) j++;
        k = 0;
    }
    long long start = min(i, j);
    return s2.substr(start, n);
}

int main() {
    cout << smallestRotation("bca") << endl;
    return 0;
}
