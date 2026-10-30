#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(N log m) time for N total values and m lists, O(m) extra space (min-heap of list heads)
vector<long long> mergeSortedLists(vector<vector<long long>> lists) {
    using Item = tuple<long long, size_t, size_t>;  // (value, list index, position)
    priority_queue<Item, vector<Item>, greater<Item>> heap;
    size_t total = 0;
    for (size_t i = 0; i < lists.size(); i++) {
        total += lists[i].size();
        if (!lists[i].empty()) heap.push({lists[i][0], i, 0});
    }
    vector<long long> merged;
    merged.reserve(total);
    while (!heap.empty()) {
        auto [value, li, pos] = heap.top();
        heap.pop();
        merged.push_back(value);
        if (pos + 1 < lists[li].size()) heap.push({lists[li][pos + 1], li, pos + 1});
    }
    return merged;
}

int main() {
    cout << mergeSortedLists(vector<vector<long long>>{vector<long long>{1, 4, 7}, vector<long long>{2, 5}, vector<long long>{3, 6, 9}}) << endl;
    return 0;
}
