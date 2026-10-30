#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long gasStation(vector<long long> gas, vector<long long> cost) {
    long long total = 0;
    long long tank = 0;
    long long start = 0;
    for (size_t i = 0; i < gas.size(); i++) {
        long long diff = gas[i] - cost[i];
        total += diff;
        tank += diff;
        if (tank < 0) {
            start = (long long)i + 1;
            tank = 0;
        }
    }
    return (total >= 0 && !gas.empty()) ? start : -1;
}

int main() {
    cout << gasStation(vector<long long>{1, 2, 3, 4, 5}, vector<long long>{3, 4, 5, 1, 2}) << endl;
    return 0;
}
