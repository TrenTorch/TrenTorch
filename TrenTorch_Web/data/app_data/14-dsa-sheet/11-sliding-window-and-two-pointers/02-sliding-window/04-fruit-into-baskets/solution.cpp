#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space (at most 3 keys live in the map)
long long totalFruit(vector<long long> fruits) {
    map<long long, long long> count;
    long long n = fruits.size();
    long long left = 0;
    long long best = 0;
    for (long long right = 0; right < n; right++) {
        count[fruits[right]]++;
        while (count.size() > 2) {
            long long gone = fruits[left];
            count[gone]--;
            if (count[gone] == 0) {
                count.erase(gone);
            }
            left++;
        }
        best = max(best, right - left + 1);
    }
    return best;
}

int main() {
    cout << totalFruit(vector<long long>{1, 2, 3, 2, 2}) << endl;
    return 0;
}
