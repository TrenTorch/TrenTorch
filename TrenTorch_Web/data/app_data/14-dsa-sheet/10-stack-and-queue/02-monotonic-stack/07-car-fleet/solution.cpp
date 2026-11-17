#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space
long long carFleet(long long target, vector<vector<long long>> cars) {
    vector<vector<long long>> sortedCars = cars;
    sort(sortedCars.begin(), sortedCars.end(), greater<vector<long long>>());
    long long fleets = 0;
    long long slowNum = 0, slowDen = 1;
    for (const auto& car : sortedCars) {
        long long num = target - car[0];
        long long den = car[1];
        if (num * slowDen > slowNum * den) {
            fleets++;
            slowNum = num;
            slowDen = den;
        }
    }
    return fleets;
}

int main() {
    cout << carFleet(12, vector<vector<long long>>{vector<long long>{10, 2}, vector<long long>{8, 4}, vector<long long>{0, 1}, vector<long long>{5, 1}, vector<long long>{3, 3}}) << endl;
    return 0;
}
