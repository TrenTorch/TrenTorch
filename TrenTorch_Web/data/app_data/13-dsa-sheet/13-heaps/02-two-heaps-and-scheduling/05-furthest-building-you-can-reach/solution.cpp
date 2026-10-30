#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space
long long furthestBuilding(vector<long long> heights, long long bricks, long long ladders) {
    priority_queue<long long, vector<long long>, greater<long long>> heap;  // climbs currently covered by ladders
    for (size_t i = 1; i < heights.size(); i++) {
        long long climb = heights[i] - heights[i - 1];
        if (climb <= 0) continue;
        heap.push(climb);
        if ((long long)heap.size() > ladders) {
            bricks -= heap.top();
            heap.pop();
            if (bricks < 0) return (long long)i - 1;
        }
    }
    return (long long)heights.size() - 1;
}

int main() {
    cout << furthestBuilding(vector<long long>{4, 2, 7, 6, 9, 14, 12}, 5, 1) << endl;
    return 0;
}
