#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space
vector<long long> sortedSquares(vector<long long> nums) {
    int n = nums.size();
    vector<long long> out(n, 0);
    int left = 0, right = n - 1;
    for (int i = n - 1; i >= 0; i--) {
        if (llabs(nums[left]) > llabs(nums[right])) {
            out[i] = nums[left] * nums[left];
            left++;
        } else {
            out[i] = nums[right] * nums[right];
            right--;
        }
    }
    return out;
}

int main() {
    cout << sortedSquares(vector<long long>{-4, -1, 0, 3, 10}) << endl;
    return 0;
}
