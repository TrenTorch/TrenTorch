#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space
long long lengthOfLis(vector<long long> nums) {
    vector<long long> tails;
    for (long long x : nums) {
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) {
            tails.push_back(x);
        } else {
            *it = x;
        }
    }
    return (long long)tails.size();
}

int main() {
    cout << lengthOfLis(vector<long long>{10, 9, 2, 5, 3, 7, 101, 18}) << endl;
    return 0;
}
