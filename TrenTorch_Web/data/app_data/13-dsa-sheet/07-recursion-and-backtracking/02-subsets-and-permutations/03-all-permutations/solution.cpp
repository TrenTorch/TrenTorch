#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

void allPermutationsGo(const vector<long long>& a, vector<bool>& used, vector<long long>& current,
                       vector<vector<long long>>& out) {
    if (current.size() == a.size()) {
        out.push_back(current);
        return;
    }
    for (size_t j = 0; j < a.size(); j++) {
        if (used[j]) continue;
        used[j] = true;
        current.push_back(a[j]);
        allPermutationsGo(a, used, current, out);
        current.pop_back();
        used[j] = false;
    }
}

// O(n! * n) time, O(n) recursion space plus the output
vector<vector<long long>> allPermutations(vector<long long> nums) {
    sort(nums.begin(), nums.end());
    vector<bool> used(nums.size(), false);
    vector<vector<long long>> out;
    vector<long long> current;
    allPermutationsGo(nums, used, current, out);
    return out;
}

int main() {
    cout << allPermutations(vector<long long>{1, 2, 3}) << endl;
    return 0;
}
