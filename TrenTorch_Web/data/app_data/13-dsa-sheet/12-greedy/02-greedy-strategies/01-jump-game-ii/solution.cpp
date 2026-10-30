#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long minJumps(vector<long long> nums) {
    long long n = nums.size();
    if (n <= 1) return 0;
    long long jumps = 0;
    long long end = 0;
    long long far = 0;
    for (long long i = 0; i < n - 1; i++) {
        far = max(far, i + nums[i]);
        if (i == far) return -1;
        if (i == end) {
            jumps++;
            end = far;
            if (end >= n - 1) break;
        }
    }
    return end >= n - 1 ? jumps : -1;
}

int main() {
    cout << minJumps(vector<long long>{2, 3, 1, 1, 4}) << endl;
    return 0;
}
