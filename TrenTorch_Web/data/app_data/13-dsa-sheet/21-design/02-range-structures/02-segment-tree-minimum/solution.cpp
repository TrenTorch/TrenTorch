#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(log n) time per operation, O(n) space
vector<long long> runSegmentTree(vector<long long> nums, vector<string> ops) {
    long long n = nums.size();
    const long long INF = LLONG_MAX;
    vector<long long> tree(2 * n, INF);
    for (long long i = 0; i < n; i++) tree[n + i] = nums[i];
    for (long long i = n - 1; i > 0; i--) tree[i] = min(tree[2 * i], tree[2 * i + 1]);
    vector<long long> out;
    for (const string& op : ops) {
        istringstream iss(op);
        string kind;
        iss >> kind;
        if (kind == "set") {
            long long i, v;
            iss >> i >> v;
            i += n;
            tree[i] = v;
            for (i /= 2; i >= 1; i /= 2) tree[i] = min(tree[2 * i], tree[2 * i + 1]);
        } else {
            long long l, r;
            iss >> l >> r;
            long long lo = l + n, hi = r + n + 1;
            long long best = INF;
            while (lo < hi) {
                if (lo & 1) best = min(best, tree[lo++]);
                if (hi & 1) best = min(best, tree[--hi]);
                lo /= 2;
                hi /= 2;
            }
            out.push_back(best);
        }
    }
    return out;
}

int main() {
    cout << runSegmentTree(vector<long long>{5, 2, 8, 1}, vector<string>{"min 0 3", "set 3 9", "min 0 3", "min 2 3"}) << endl;
    return 0;
}
