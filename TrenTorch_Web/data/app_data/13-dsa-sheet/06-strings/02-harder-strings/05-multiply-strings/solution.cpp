#include <bits/stdc++.h>
using namespace std;

// O(n * m) time, O(n + m) space
string multiplyStrings(string a, string b) {
    vector<long long> acc(a.size() + b.size(), 0);
    for (long long i = (long long)a.size() - 1; i >= 0; i--) {
        for (long long j = (long long)b.size() - 1; j >= 0; j--) {
            acc[i + j + 1] += (a[i] - '0') * (b[j] - '0');
        }
    }
    for (long long k = (long long)acc.size() - 1; k > 0; k--) {
        acc[k - 1] += acc[k] / 10;
        acc[k] %= 10;
    }
    size_t start = 0;
    while (start + 1 < acc.size() && acc[start] == 0) start++;
    string out;
    for (size_t k = start; k < acc.size(); k++) out += char('0' + acc[k]);
    return out;
}

int main() {
    cout << multiplyStrings("123", "456") << endl;
    return 0;
}
