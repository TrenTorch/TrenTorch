#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n log k) time, O(k) space
vector<long long> sortKSorted(vector<long long> nums, long long k) {
    priority_queue<long long, vector<long long>, greater<long long>> heap;
    size_t m = min(nums.size(), (size_t)k + 1);
    for (size_t i = 0; i < m; i++) heap.push(nums[i]);
    vector<long long> out;
    for (size_t i = m; i < nums.size(); i++) {
        heap.push(nums[i]);
        out.push_back(heap.top());
        heap.pop();
    }
    while (!heap.empty()) {
        out.push_back(heap.top());
        heap.pop();
    }
    return out;
}

int main() {
    cout << sortKSorted(vector<long long>{6, 5, 3, 2, 8, 10, 9}, 3) << endl;
    return 0;
}
