#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O((n + m) log n) time for n items and m operations, O(n) space
vector<long long> runFenwick(vector<long long> nums, vector<string> ops) {
    long long n = nums.size();
    vector<long long> tree(n + 1, 0), values = nums;
    auto add = [&](long long i, long long delta) {
        for (i++; i <= n; i += i & -i) tree[i] += delta;
    };
    auto prefix = [&](long long i) {
        long long total = 0;
        for (; i > 0; i -= i & -i) total += tree[i];
        return total;
    };
    for (long long i = 0; i < n; i++) add(i, nums[i]);
    vector<long long> out;
    for (const string& op : ops) {
        istringstream iss(op);
        string kind;
        iss >> kind;
        if (kind == "set") {
            long long i, v;
            iss >> i >> v;
            add(i, v - values[i]);
            values[i] = v;
        } else {
            long long left, right;
            iss >> left >> right;
            out.push_back(prefix(right + 1) - prefix(left));
        }
    }
    return out;
}

int main() {
    cout << runFenwick(vector<long long>{1, 2, 3, 4}, vector<string>{"sum 0 3", "set 1 10", "sum 0 2", "sum 1 1"}) << endl;
    return 0;
}
