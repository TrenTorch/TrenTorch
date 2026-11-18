#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) extra space
long long secondLargest(vector<long long> nums) {
    bool hasLargest = false, hasSecond = false;
    long long largest = 0, second = 0;
    for (long long x : nums) {
        if (!hasLargest || x > largest) {
            second = largest;
            hasSecond = hasLargest;
            largest = x;
            hasLargest = true;
        } else if (x < largest && (!hasSecond || x > second)) {
            second = x;
            hasSecond = true;
        }
    }
    return hasSecond ? second : -1;
}

int main() {
    cout << secondLargest(vector<long long>{4, 9, 9, 6}) << endl;
    return 0;
}
