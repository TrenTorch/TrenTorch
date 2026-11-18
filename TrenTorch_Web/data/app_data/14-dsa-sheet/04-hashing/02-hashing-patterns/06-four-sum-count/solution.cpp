#include <bits/stdc++.h>
using namespace std;

// O(n^2) expected time, O(n^2) space (n = list length; pair sums of a and b are hashed)
long long fourSumCount(vector<long long> a, vector<long long> b, vector<long long> c, vector<long long> d) {
    unordered_map<long long, long long> sums;
    sums.reserve(a.size() * b.size() * 2 + 1);
    for (long long x : a) {
        for (long long y : b) sums[x + y]++;
    }
    long long total = 0;
    for (long long z : c) {
        for (long long w : d) {
            auto it = sums.find(-(z + w));
            if (it != sums.end()) total += it->second;
        }
    }
    return total;
}

int main() {
    cout << fourSumCount(vector<long long>{1, 2}, vector<long long>{-2, -1}, vector<long long>{-1, 2}, vector<long long>{0, 2}) << endl;
    return 0;
}
