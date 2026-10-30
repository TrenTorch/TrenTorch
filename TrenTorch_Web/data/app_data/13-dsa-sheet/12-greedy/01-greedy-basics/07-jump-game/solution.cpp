#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
bool canJump(vector<long long> nums) {
    long long far = 0;
    long long n = nums.size();
    for (long long i = 0; i < n; i++) {
        if (i > far) return false;
        far = max(far, i + nums[i]);
    }
    return true;
}

int main() {
    cout << boolalpha << canJump(vector<long long>{2, 3, 1, 1, 4}) << endl;
    return 0;
}
