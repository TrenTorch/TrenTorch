#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space
vector<long long> nextGreaterCircular(vector<long long> nums) {
    int n = nums.size();
    vector<long long> out(n, -1);
    vector<int> stack;
    for (int i = 0; i < 2 * n; i++) {
        long long x = nums[i % n];
        while (!stack.empty() && nums[stack.back()] < x) {
            out[stack.back()] = x;
            stack.pop_back();
        }
        if (i < n) stack.push_back(i);
    }
    return out;
}

int main() {
    cout << nextGreaterCircular(vector<long long>{1, 2, 1}) << endl;
    return 0;
}
