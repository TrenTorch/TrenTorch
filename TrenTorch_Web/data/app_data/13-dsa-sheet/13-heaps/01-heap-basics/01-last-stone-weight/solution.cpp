#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space
long long lastStoneWeight(vector<long long> stones) {
    priority_queue<long long> heap(stones.begin(), stones.end());
    while (heap.size() > 1) {
        long long a = heap.top();
        heap.pop();
        long long b = heap.top();
        heap.pop();
        if (a != b) heap.push(a - b);
    }
    return heap.empty() ? 0 : heap.top();
}

int main() {
    cout << lastStoneWeight(vector<long long>{2, 7, 4, 1, 8, 1}) << endl;
    return 0;
}
