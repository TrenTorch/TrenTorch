#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long trapWater(vector<long long> heights) {
    long long left = 0;
    long long right = (long long)heights.size() - 1;
    long long left_max = 0, right_max = 0, total = 0;
    while (left < right) {
        if (heights[left] < heights[right]) {
            left_max = max(left_max, heights[left]);
            total += left_max - heights[left];
            left++;
        } else {
            right_max = max(right_max, heights[right]);
            total += right_max - heights[right];
            right--;
        }
    }
    return total;
}

int main() {
    cout << trapWater(vector<long long>{0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1}) << endl;
    return 0;
}
