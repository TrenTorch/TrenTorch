#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
long long sumSubarrayMins(vector<long long> arr) {
    const long long MOD = 1000000007LL;
    int n = arr.size();
    vector<int> left(n), right(n);
    vector<int> stack;
    for (int i = 0; i < n; i++) {
        while (!stack.empty() && arr[stack.back()] >= arr[i]) stack.pop_back();
        left[i] = stack.empty() ? -1 : stack.back();
        stack.push_back(i);
    }
    stack.clear();
    for (int i = n - 1; i >= 0; i--) {
        while (!stack.empty() && arr[stack.back()] > arr[i]) stack.pop_back();
        right[i] = stack.empty() ? n : stack.back();
        stack.push_back(i);
    }
    long long total = 0;
    for (int i = 0; i < n; i++) {
        long long term = arr[i] * (long long)(i - left[i]) * (long long)(right[i] - i) % MOD;
        total = (total + term) % MOD;
    }
    return total;
}

int main() {
    cout << sumSubarrayMins(vector<long long>{3, 1, 2, 4}) << endl;
    return 0;
}
