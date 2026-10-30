#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n log k) time, O(k) space (two heaps with lazy deletion)
vector<double> medianSlidingWindow(vector<long long> nums, long long k) {
    priority_queue<long long> small;  // max-heap of the lower half
    priority_queue<long long, vector<long long>, greater<long long>> large;  // min-heap of the upper half
    unordered_map<long long, long long> delayed;  // value -> copies that left the window but are still in a heap
    long long sizes[2] = {0, 0};  // live sizes of small and large

    // Drop stale tops of a heap whose value is pending deletion.
    auto clean = [&](auto& heap) {
        while (!heap.empty()) {
            long long value = heap.top();
            auto it = delayed.find(value);
            if (it != delayed.end() && it->second > 0) {
                it->second--;
                heap.pop();
            } else {
                break;
            }
        }
    };

    auto balance = [&]() {
        if (sizes[0] > sizes[1] + 1) {
            large.push(small.top());
            small.pop();
            sizes[0]--;
            sizes[1]++;
            clean(small);
        } else if (sizes[0] < sizes[1]) {
            small.push(large.top());
            large.pop();
            sizes[1]--;
            sizes[0]++;
            clean(large);
        }
    };

    auto add = [&](long long x) {
        if (small.empty() || x <= small.top()) {
            small.push(x);
            sizes[0]++;
        } else {
            large.push(x);
            sizes[1]++;
        }
        balance();
    };

    auto remove = [&](long long x) {
        delayed[x]++;
        if (x <= small.top()) {
            sizes[0]--;
            if (x == small.top()) clean(small);
        } else {
            sizes[1]--;
            if (x == large.top()) clean(large);
        }
        balance();
    };

    auto median = [&]() -> double {
        if (k % 2) return (double)small.top();
        return (double)(small.top() + large.top()) / 2.0;
    };

    for (long long i = 0; i < k; i++) add(nums[i]);
    vector<double> out = {median()};
    for (size_t i = k; i < nums.size(); i++) {
        add(nums[i]);
        remove(nums[i - k]);
        out.push_back(median());
    }
    return out;
}

int main() {
    cout << medianSlidingWindow(vector<long long>{1, 3, -1, -3, 5, 3, 6, 7}, 3) << endl;
    return 0;
}
