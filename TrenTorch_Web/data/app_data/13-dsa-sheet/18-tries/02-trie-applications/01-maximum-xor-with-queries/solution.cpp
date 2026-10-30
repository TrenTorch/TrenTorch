#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O((N + Q) * 30) time, O(N * 30) space
vector<long long> maxXorQueries(vector<long long> nums, vector<long long> queries) {
    vector<array<int, 2>> nxt(1);
    nxt[0] = {-1, -1};
    for (long long n : nums) {
        int node = 0;
        for (int b = 29; b >= 0; b--) {
            int bit = (n >> b) & 1;
            if (nxt[node][bit] < 0) {
                nxt[node][bit] = static_cast<int>(nxt.size());
                nxt.push_back({-1, -1});
            }
            node = nxt[node][bit];
        }
    }
    vector<long long> out;
    for (long long x : queries) {
        int node = 0;
        long long best = 0;
        for (int b = 29; b >= 0; b--) {
            int bit = (x >> b) & 1;
            if (nxt[node][1 - bit] >= 0) {
                best |= 1LL << b;
                node = nxt[node][1 - bit];
            } else {
                node = nxt[node][bit];
            }
        }
        out.push_back(best);
    }
    return out;
}

int main() {
    cout << maxXorQueries(vector<long long>{0, 1, 2, 3, 4}, vector<long long>{3, 5}) << endl;
    return 0;
}
