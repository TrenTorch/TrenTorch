#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(1) extra space for the vote, plus O(n) for the two verification counts
vector<long long> majorityElementThirds(vector<long long> nums) {
    bool hasA = false, hasB = false;
    long long a = 0, b = 0, ca = 0, cb = 0;
    for (long long x : nums) {
        if (hasA && x == a) {
            ca++;
        } else if (hasB && x == b) {
            cb++;
        } else if (ca == 0) {
            a = x;
            hasA = true;
            ca = 1;
        } else if (cb == 0) {
            b = x;
            hasB = true;
            cb = 1;
        } else {
            ca--;
            cb--;
        }
    }
    long long n = nums.size();
    vector<long long> candidates;
    if (hasA) candidates.push_back(a);
    if (hasB && (!hasA || b != a)) candidates.push_back(b);
    vector<long long> out;
    for (long long v : candidates) {
        long long occurrences = count(nums.begin(), nums.end(), v);
        if (occurrences * 3 > n) out.push_back(v);
    }
    sort(out.begin(), out.end());
    return out;
}

int main() {
    cout << majorityElementThirds(vector<long long>{3, 2, 3}) << endl;
    return 0;
}
