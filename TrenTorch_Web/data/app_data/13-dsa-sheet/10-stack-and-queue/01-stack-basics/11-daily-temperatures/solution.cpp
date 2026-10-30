#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space
vector<long long> dailyTemperatures(vector<long long> temps) {
    int n = temps.size();
    vector<long long> out(n, 0);
    vector<int> stack;
    for (int i = 0; i < n; i++) {
        while (!stack.empty() && temps[stack.back()] < temps[i]) {
            int j = stack.back();
            stack.pop_back();
            out[j] = i - j;
        }
        stack.push_back(i);
    }
    return out;
}

int main() {
    cout << dailyTemperatures(vector<long long>{73, 74, 75, 71, 69, 72, 76, 73}) << endl;
    return 0;
}
