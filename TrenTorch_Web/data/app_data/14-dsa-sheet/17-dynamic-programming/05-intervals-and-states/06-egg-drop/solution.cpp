#include <bits/stdc++.h>
using namespace std;

// O(eggs * answer) time, O(eggs) space
long long eggDrop(long long eggs, long long floors) {
    if (floors == 0 || eggs == 0) return 0;
    int E = eggs;
    vector<long long> reach(E + 1, 0);
    long long drops = 0;
    while (reach[E] < floors) {
        drops++;
        for (int e = E; e >= 1; --e) {
            reach[e] = reach[e - 1] + reach[e] + 1;
        }
    }
    return drops;
}

int main() {
    cout << eggDrop(2, 6) << endl;
    return 0;
}
