#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O((n + m) log k) time, O(k) space where n = len(nums) and m = len(adds)
vector<long long> kthLargestStream(long long k, vector<long long> nums, vector<long long> adds) {
    priority_queue<long long, vector<long long>, greater<long long>> heap;
    for (long long x : nums) {
        heap.push(x);
        if ((long long)heap.size() > k) heap.pop();
    }
    vector<long long> out;
    for (long long x : adds) {
        heap.push(x);
        if ((long long)heap.size() > k) heap.pop();
        out.push_back(heap.top());
    }
    return out;
}

int main() {
    cout << kthLargestStream(3, vector<long long>{4, 5, 8, 2}, vector<long long>{3, 5, 10, 9, 4}) << endl;
    return 0;
}
