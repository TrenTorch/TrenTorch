#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(1) space
vector<long long> maxSubarrayRange(vector<long long> nums) {
    long long bestSum = nums[0], bestStart = 0, bestEnd = 0;
    long long current = nums[0];
    long long start = 0;
    long long n = nums.size();
    for (long long i = 1; i < n; i++) {
        if (current < 0) {
            current = nums[i];
            start = i;
        } else {
            current += nums[i];
        }
        if (current > bestSum) {
            bestSum = current;
            bestStart = start;
            bestEnd = i;
        }
    }
    return {bestSum, bestStart, bestEnd};
}

int main() {
    cout << maxSubarrayRange(vector<long long>{-2, 1, -3, 4, -1, 2, 1, -5, 4}) << endl;
    return 0;
}
