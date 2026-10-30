#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

void uniquePermutationsGo(const vector<long long>& a, vector<bool>& used, vector<long long>& current,
                          vector<vector<long long>>& out) {
    if (current.size() == a.size()) {
        out.push_back(current);
        return;
    }
    for (size_t j = 0; j < a.size(); j++) {
        if (used[j] || (j > 0 && a[j] == a[j - 1] && !used[j - 1])) continue;
        used[j] = true;
        current.push_back(a[j]);
        uniquePermutationsGo(a, used, current, out);
        current.pop_back();
        used[j] = false;
    }
}

// O(n * n!) time worst case, O(n) recursion space plus the output
vector<vector<long long>> uniquePermutations(vector<long long> nums) {
    sort(nums.begin(), nums.end());
    vector<bool> used(nums.size(), false);
    vector<vector<long long>> out;
    vector<long long> current;
    uniquePermutationsGo(nums, used, current, out);
    return out;
}

int main() {
    cout << uniquePermutations(vector<long long>{1, 1, 2}) << endl;
    return 0;
}
