#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space
bool isNStraightHand(vector<long long> hand, long long groupSize) {
    if ((long long)hand.size() % groupSize != 0) return false;
    map<long long, long long> count;
    for (long long x : hand) count[x]++;
    priority_queue<long long, vector<long long>, greater<long long>> heap;  // keys still holding cards
    for (auto& kv : count) heap.push(kv.first);
    while (!heap.empty()) {
        long long start = heap.top();
        for (long long x = start; x < start + groupSize; x++) {
            auto it = count.find(x);
            if (it == count.end() || it->second == 0) return false;
            if (--it->second == 0) {
                if (x != heap.top()) return false;
                heap.pop();
            }
        }
    }
    return true;
}

int main() {
    cout << boolalpha << isNStraightHand(vector<long long>{1, 2, 3, 6, 2, 3, 4, 7, 8}, 3) << endl;
    return 0;
}
