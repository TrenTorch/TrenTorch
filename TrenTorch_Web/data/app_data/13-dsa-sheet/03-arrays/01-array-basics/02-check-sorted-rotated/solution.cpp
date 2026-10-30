#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) extra space
bool checkSortedRotated(vector<long long> nums) {
    size_t n = nums.size();
    if (n == 0) return true;
    size_t drops = 0;
    for (size_t i = 0; i < n; i++) {
        if (nums[i] > nums[(i + 1) % n]) drops++;
    }
    return drops <= 1;
}

int main() {
    cout << boolalpha << checkSortedRotated(vector<long long>{3, 4, 5, 1, 2}) << endl;
    return 0;
}
