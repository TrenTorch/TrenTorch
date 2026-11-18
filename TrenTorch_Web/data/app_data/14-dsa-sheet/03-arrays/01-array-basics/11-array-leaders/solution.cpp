#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space
vector<long long> arrayLeaders(vector<long long> nums) {
    vector<long long> out;
    bool hasBest = false;
    long long best = 0;
    for (int i = (int)nums.size() - 1; i >= 0; i--) {
        if (!hasBest || nums[i] > best) {
            out.push_back(nums[i]);
            best = nums[i];
            hasBest = true;
        }
    }
    reverse(out.begin(), out.end());
    return out;
}

int main() {
    cout << arrayLeaders(vector<long long>{16, 17, 4, 3, 5, 2}) << endl;
    return 0;
}
