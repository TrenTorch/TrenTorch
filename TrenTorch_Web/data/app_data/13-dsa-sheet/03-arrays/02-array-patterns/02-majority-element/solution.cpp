#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long majorityElement(vector<long long> nums) {
    if (nums.empty()) return -1;
    long long candidate = 0, cnt = 0;
    for (long long x : nums) {
        if (cnt == 0) candidate = x;
        cnt += (x == candidate) ? 1 : -1;
    }
    long long occurrences = count(nums.begin(), nums.end(), candidate);
    if (occurrences > (long long)nums.size() / 2) return candidate;
    return -1;
}

int main() {
    cout << majorityElement(vector<long long>{2, 2, 1, 1, 2, 2, 3}) << endl;
    return 0;
}
