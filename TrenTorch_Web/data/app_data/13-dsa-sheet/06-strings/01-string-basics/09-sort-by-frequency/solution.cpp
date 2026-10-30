#include <bits/stdc++.h>
using namespace std;

// O(n + K log K) time, where K <= 256 is the number of distinct characters; O(n) space
string sortByFrequency(string s) {
    vector<long long> counts(256, 0);
    for (unsigned char ch : s) {
        counts[ch]++;
    }
    vector<unsigned char> order;
    for (int c = 0; c < 256; c++) {
        if (counts[c] > 0) {
            order.push_back((unsigned char)c);
        }
    }
    sort(order.begin(), order.end(), [&](unsigned char a, unsigned char b) {
        if (counts[a] != counts[b]) {
            return counts[a] > counts[b];
        }
        return a < b;
    });
    string out;
    for (unsigned char ch : order) {
        out.append(static_cast<size_t>(counts[ch]), (char)ch);
    }
    return out;
}

int main() {
    cout << sortByFrequency("tree") << endl;
    return 0;
}
