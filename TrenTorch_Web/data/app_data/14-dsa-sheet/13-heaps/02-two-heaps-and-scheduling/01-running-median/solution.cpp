#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n log n) time, O(n) space
vector<double> runningMedian(vector<long long> nums) {
    priority_queue<long long> low;  // max-heap of the lower half
    priority_queue<long long, vector<long long>, greater<long long>> high;  // min-heap of the upper half
    vector<double> out;
    for (long long x : nums) {
        low.push(x);
        high.push(low.top());
        low.pop();
        if (high.size() > low.size()) {
            low.push(high.top());
            high.pop();
        }
        if (low.size() > high.size()) out.push_back((double)low.top());
        else out.push_back((double)(low.top() + high.top()) / 2.0);
    }
    return out;
}

int main() {
    cout << runningMedian(vector<long long>{5, 15, 1, 3}) << endl;
    return 0;
}
