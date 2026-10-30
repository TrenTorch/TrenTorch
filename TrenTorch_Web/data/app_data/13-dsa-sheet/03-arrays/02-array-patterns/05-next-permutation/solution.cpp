#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(1) extra space (besides the copy)
vector<long long> nextPermutation(vector<long long> nums) {
    vector<long long> a = nums;
    int n = a.size();
    if (n == 0) return a;
    int i = n - 2;
    while (i >= 0 && a[i] >= a[i + 1]) i--;
    if (i >= 0) {
        int j = n - 1;
        while (a[j] <= a[i]) j--;
        swap(a[i], a[j]);
    }
    reverse(a.begin() + (i + 1), a.end());
    return a;
}

int main() {
    cout << nextPermutation(vector<long long>{1, 2, 3}) << endl;
    return 0;
}
