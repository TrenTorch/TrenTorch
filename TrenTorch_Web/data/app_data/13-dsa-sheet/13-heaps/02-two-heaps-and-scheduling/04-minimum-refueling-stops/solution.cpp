#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space
long long minRefuelStops(long long target, long long startFuel, vector<vector<long long>> stations) {
    priority_queue<long long> heap;  // max-heap of fuel at stations passed so far
    long long reach = startFuel;
    long long stops = 0;
    size_t i = 0;
    while (reach < target) {
        while (i < stations.size() && stations[i][0] <= reach) {
            heap.push(stations[i][1]);
            i++;
        }
        if (heap.empty()) return -1;
        reach += heap.top();
        heap.pop();
        stops++;
    }
    return stops;
}

int main() {
    cout << minRefuelStops(100, 10, vector<vector<long long>>{vector<long long>{10, 60}, vector<long long>{20, 30}, vector<long long>{30, 30}, vector<long long>{60, 40}}) << endl;
    return 0;
}
