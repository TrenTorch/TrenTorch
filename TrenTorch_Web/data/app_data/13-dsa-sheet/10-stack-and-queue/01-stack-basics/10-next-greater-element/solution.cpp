#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space
vector<long long> nextGreater(vector<long long> nums) {
    vector<long long> out(nums.size(), -1);
    vector<size_t> stk;
    for (size_t i = 0; i < nums.size(); i++) {
        while (!stk.empty() && nums[stk.back()] < nums[i]) {
            out[stk.back()] = nums[i];
            stk.pop_back();
        }
        stk.push_back(i);
    }
    return out;
}

int main() {
    cout << nextGreater(vector<long long>{2, 1, 2, 4, 3}) << endl;
    return 0;
}
