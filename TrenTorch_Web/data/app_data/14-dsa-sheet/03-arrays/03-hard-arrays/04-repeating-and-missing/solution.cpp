#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(1) extra space
vector<long long> repeatingAndMissing(vector<long long> nums) {
    long long n = nums.size();
    long long diff = 0, squareDiff = 0;
    for (long long x : nums) {
        diff += x;
        squareDiff += x * x;
    }
    diff -= n * (n + 1) / 2;
    squareDiff -= n * (n + 1) * (2 * n + 1) / 6;
    long long plus = squareDiff / diff;
    return {(plus + diff) / 2, (plus - diff) / 2};
}

int main() {
    cout << repeatingAndMissing(vector<long long>{3, 1, 2, 5, 3}) << endl;
    return 0;
}
