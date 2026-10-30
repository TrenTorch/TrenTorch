#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(N log k) time, O(k) heap space plus the output, where N is the total number of values
vector<long long> mergeKArrays(vector<vector<long long>> arrays) {
    using Node = tuple<long long, size_t, size_t>;  // (value, array index, position)
    priority_queue<Node, vector<Node>, greater<Node>> heap;
    for (size_t i = 0; i < arrays.size(); i++) {
        if (!arrays[i].empty()) heap.emplace(arrays[i][0], i, 0);
    }
    vector<long long> out;
    while (!heap.empty()) {
        auto [value, i, j] = heap.top();
        heap.pop();
        out.push_back(value);
        if (j + 1 < arrays[i].size()) heap.emplace(arrays[i][j + 1], i, j + 1);
    }
    return out;
}

int main() {
    cout << mergeKArrays(vector<vector<long long>>{vector<long long>{1, 4, 5}, vector<long long>{1, 3, 4}, vector<long long>{2, 6}}) << endl;
    return 0;
}
