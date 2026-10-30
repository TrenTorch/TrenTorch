#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) extra space (Floyd cycle detection, nums not modified)
long long findDuplicate(vector<long long> nums) {
    long long slow = nums[0];
    long long fast = nums[0];
    while (true) {
        slow = nums[slow];
        fast = nums[nums[fast]];
        if (slow == fast) {
            break;
        }
    }
    slow = nums[0];
    while (slow != fast) {
        slow = nums[slow];
        fast = nums[fast];
    }
    return slow;
}

int main() {
    cout << findDuplicate(vector<long long>{1, 3, 4, 2, 2}) << endl;
    return 0;
}
