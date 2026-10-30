#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(1) extra space (one pass, Dutch national flag)
vector<long long> sortColors(vector<long long> nums) {
    size_t low = 0, mid = 0, high = nums.size();
    while (mid < high) {
        if (nums[mid] == 0) {
            swap(nums[low++], nums[mid++]);
        } else if (nums[mid] == 1) {
            mid++;
        } else {
            swap(nums[mid], nums[--high]);
        }
    }
    return nums;
}

int main() {
    cout << sortColors(vector<long long>{2, 0, 2, 1, 1, 0}) << endl;
    return 0;
}
