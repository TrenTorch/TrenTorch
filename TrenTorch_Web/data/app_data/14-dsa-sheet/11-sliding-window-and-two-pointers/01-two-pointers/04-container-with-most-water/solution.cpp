#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long maxWater(vector<long long> heights) {
    int left = 0, right = (int)heights.size() - 1;
    long long best = 0;
    while (left < right) {
        best = max(best, min(heights[left], heights[right]) * (long long)(right - left));
        if (heights[left] < heights[right]) left++;
        else right--;
    }
    return best;
}

int main() {
    cout << maxWater(vector<long long>{1, 8, 6, 2, 5, 4, 8, 3, 7}) << endl;
    return 0;
}
