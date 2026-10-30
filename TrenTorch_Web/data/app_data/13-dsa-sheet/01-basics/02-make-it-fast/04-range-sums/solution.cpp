#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n + q) time, O(n) space (prefix sums)
vector<long long> rangeSums(vector<long long> nums, vector<vector<long long>> queries) {
    vector<long long> prefix(nums.size() + 1, 0);
    for (size_t i = 0; i < nums.size(); i++) prefix[i + 1] = prefix[i] + nums[i];
    vector<long long> answers;
    answers.reserve(queries.size());
    for (const auto& q : queries) {
        answers.push_back(prefix[q[1] + 1] - prefix[q[0]]);
    }
    return answers;
}

int main() {
    cout << rangeSums(vector<long long>{1, 2, 3, 4, 5}, vector<vector<long long>>{vector<long long>{0, 4}, vector<long long>{1, 3}, vector<long long>{2, 2}}) << endl;
    return 0;
}
