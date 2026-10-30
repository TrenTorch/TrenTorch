#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long minCostClimbing(vector<long long> cost) {
    long long prev2 = 0, prev1 = 0;
    for (size_t i = 2; i <= cost.size(); i++) {
        long long next = min(prev1 + cost[i - 1], prev2 + cost[i - 2]);
        prev2 = prev1;
        prev1 = next;
    }
    return prev1;
}

int main() {
    cout << minCostClimbing(vector<long long>{10, 15, 20}) << endl;
    return 0;
}
