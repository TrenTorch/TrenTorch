#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(k log min(k, n1)) time, O(min(k, n1)) heap space
vector<long long> kSmallestPairSums(vector<long long> nums1, vector<long long> nums2, long long k) {
    vector<long long> out;
    if (nums1.empty() || nums2.empty() || k <= 0) return out;
    using Node = tuple<long long, size_t, size_t>;  // (sum, index in nums1, index in nums2)
    priority_queue<Node, vector<Node>, greater<Node>> heap;
    size_t m = min(nums1.size(), (size_t)k);
    for (size_t i = 0; i < m; i++) heap.emplace(nums1[i] + nums2[0], i, 0);
    while (!heap.empty() && (long long)out.size() < k) {
        auto [total, i, j] = heap.top();
        heap.pop();
        out.push_back(total);
        if (j + 1 < nums2.size()) heap.emplace(nums1[i] + nums2[j + 1], i, j + 1);
    }
    return out;
}

int main() {
    cout << kSmallestPairSums(vector<long long>{1, 7, 11}, vector<long long>{2, 4, 6}, 3) << endl;
    return 0;
}
