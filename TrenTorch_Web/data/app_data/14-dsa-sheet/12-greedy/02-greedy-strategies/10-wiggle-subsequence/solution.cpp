#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long wiggleLength(vector<long long> nums) {
    if (nums.empty()) return 0;
    long long length = 1;
    long long direction = 0;
    for (size_t i = 1; i < nums.size(); i++) {
        long long diff = nums[i] - nums[i - 1];
        if (diff > 0 && direction <= 0) {
            length++;
            direction = 1;
        } else if (diff < 0 && direction >= 0) {
            length++;
            direction = -1;
        }
    }
    return length;
}

int main() {
    cout << wiggleLength(vector<long long>{1, 7, 4, 9, 2, 5}) << endl;
    return 0;
}
