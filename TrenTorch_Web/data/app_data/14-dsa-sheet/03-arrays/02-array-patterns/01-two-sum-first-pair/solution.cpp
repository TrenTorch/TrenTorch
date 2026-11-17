#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space
vector<long long> twoSumFirstPair(vector<long long> nums, long long target) {
    unordered_map<long long, long long> first;
    bool found = false;
    long long bestI = 0, bestJ = 0;
    for (long long j = 0; j < (long long)nums.size(); j++) {
        long long x = nums[j];
        auto it = first.find(target - x);
        if (it != first.end()) {
            long long i = it->second;
            if (!found || make_pair(i, j) < make_pair(bestI, bestJ)) {
                found = true;
                bestI = i;
                bestJ = j;
            }
        }
        if (first.find(x) == first.end()) first[x] = j;
    }
    if (!found) return {-1, -1};
    return {bestI, bestJ};
}

int main() {
    cout << twoSumFirstPair(vector<long long>{1, 6, 5, 3, 8}, 9) << endl;
    return 0;
}
