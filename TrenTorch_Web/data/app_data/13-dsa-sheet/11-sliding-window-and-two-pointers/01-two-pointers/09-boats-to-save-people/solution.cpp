#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space (sorting copy)
long long boatsNeeded(vector<long long> people, long long limit) {
    vector<long long> a = people;
    sort(a.begin(), a.end());
    long long light = 0;
    long long heavy = (long long)a.size() - 1;
    long long boats = 0;
    while (light <= heavy) {
        if (a[light] + a[heavy] <= limit) {
            light++;
        }
        heavy--;
        boats++;
    }
    return boats;
}

int main() {
    cout << boatsNeeded(vector<long long>{3, 2, 2, 1}, 3) << endl;
    return 0;
}
