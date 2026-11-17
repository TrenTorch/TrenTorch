#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n log n) time to build, O(1) time per query, O(n log n) space
vector<long long> rangeMinimums(vector<long long> nums, vector<vector<long long>> queries) {
    long long n = nums.size();
    vector<vector<long long>> table;
    table.push_back(nums);
    for (int k = 1; (1LL << k) <= n; k++) {
        const vector<long long>& prev = table.back();
        long long half = 1LL << (k - 1);
        vector<long long> row(prev.size() - half);
        for (size_t i = 0; i < row.size(); i++) row[i] = min(prev[i], prev[i + half]);
        table.push_back(row);
    }
    vector<long long> out;
    for (const auto& q : queries) {
        long long left = q[0], right = q[1];
        long long len = right - left + 1;
        int level = 0;
        while ((2LL << level) <= len) level++;
        const vector<long long>& row = table[level];
        out.push_back(min(row[left], row[right - (1LL << level) + 1]));
    }
    return out;
}

int main() {
    cout << rangeMinimums(vector<long long>{5, 2, 8, 1, 9}, vector<vector<long long>>{vector<long long>{0, 4}, vector<long long>{1, 2}, vector<long long>{2, 2}}) << endl;
    return 0;
}
