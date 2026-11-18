#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(k) space
vector<long long> slidingWindowMax(vector<long long> nums, long long k) {
    int n = nums.size();
    deque<int> window;
    vector<long long> out;
    for (int i = 0; i < n; i++) {
        while (!window.empty() && nums[window.back()] <= nums[i]) window.pop_back();
        window.push_back(i);
        if ((long long)window.front() <= i - k) window.pop_front();
        if (i >= k - 1) out.push_back(nums[window.front()]);
    }
    return out;
}

int main() {
    cout << slidingWindowMax(vector<long long>{1, 3, -1, -3, 5, 3, 6, 7}, 3) << endl;
    return 0;
}
