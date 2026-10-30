#include <bits/stdc++.h>
using namespace std;

// O(n + d log d) time, where d is the number of distinct characters; O(d) space
vector<pair<char, long long>> topCharacters(string s, long long k) {
    vector<long long> count(256, 0);
    for (char c : s) count[(unsigned char)c]++;
    vector<pair<char, long long>> ranked;
    for (int c = 0; c < 256; c++) {
        if (count[c] > 0) ranked.push_back({(char)c, count[c]});
    }
    sort(ranked.begin(), ranked.end(), [](const pair<char, long long>& a, const pair<char, long long>& b) {
        if (a.second != b.second) return a.second > b.second;
        return (unsigned char)a.first < (unsigned char)b.first;
    });
    if (k <= 0) return {};
    if ((long long)ranked.size() > k) ranked.resize((size_t)k);
    return ranked;
}

int main() {
    return 0;
}
