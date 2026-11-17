#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space
vector<long long> stockSpan(vector<long long> prices) {
    int n = prices.size();
    vector<long long> out;
    vector<int> stack;
    for (int i = 0; i < n; i++) {
        while (!stack.empty() && prices[stack.back()] <= prices[i]) stack.pop_back();
        out.push_back(stack.empty() ? i + 1 : i - stack.back());
        stack.push_back(i);
    }
    return out;
}

int main() {
    cout << stockSpan(vector<long long>{100, 80, 60, 70, 60, 75, 85}) << endl;
    return 0;
}
