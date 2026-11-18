#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
long long shortestSubarraySumK(vector<long long> nums, long long k) {
    int n = nums.size();
    vector<long long> prefix(n + 1, 0);
    for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
    long long best = n + 1;
    deque<int> window;
    for (int b = 0; b <= n; b++) {
        while (!window.empty() && prefix[b] - prefix[window.front()] >= k) {
            best = min(best, (long long)(b - window.front()));
            window.pop_front();
        }
        while (!window.empty() && prefix[window.back()] >= prefix[b]) window.pop_back();
        window.push_back(b);
    }
    return best <= n ? best : -1;
}

int main() {
    cout << shortestSubarraySumK(vector<long long>{2, -1, 2}, 3) << endl;
    return 0;
}
