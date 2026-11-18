#include <bits/stdc++.h>
using namespace std;

// O(max(n, m)) time, O(max(n, m)) space
string addBinary(string a, string b) {
    string out;
    long long i = (long long)a.size() - 1, j = (long long)b.size() - 1, carry = 0;
    while (i >= 0 || j >= 0 || carry) {
        long long total = carry;
        if (i >= 0) {
            total += a[i] - '0';
            i--;
        }
        if (j >= 0) {
            total += b[j] - '0';
            j--;
        }
        out += (char)('0' + total % 2);
        carry = total / 2;
    }
    reverse(out.begin(), out.end());
    return out;
}

int main() {
    cout << addBinary("11", "1") << endl;
    return 0;
}
