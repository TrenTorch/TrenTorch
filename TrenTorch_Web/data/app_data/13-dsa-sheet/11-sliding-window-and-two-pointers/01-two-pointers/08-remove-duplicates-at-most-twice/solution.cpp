#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space (output copy)
vector<long long> keepAtMostTwice(vector<long long> nums) {
    vector<long long> a = nums;
    size_t write = 0;
    for (size_t read = 0; read < a.size(); read++) {
        if (write < 2 || a[read] != a[write - 2]) {
            a[write] = a[read];
            write++;
        }
    }
    a.resize(write);
    return a;
}

int main() {
    cout << keepAtMostTwice(vector<long long>{1, 1, 1, 2, 2, 3}) << endl;
    return 0;
}
