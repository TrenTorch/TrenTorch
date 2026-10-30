#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space
long long connectRopes(vector<long long> ropes) {
    priority_queue<long long, vector<long long>, greater<long long>> heap;
    for (long long r : ropes) heap.push(r);
    long long total = 0;
    while (heap.size() > 1) {
        long long a = heap.top();
        heap.pop();
        long long b = heap.top();
        heap.pop();
        long long joined = a + b;
        total += joined;
        heap.push(joined);
    }
    return total;
}

int main() {
    cout << connectRopes(vector<long long>{4, 3, 2, 6}) << endl;
    return 0;
}
