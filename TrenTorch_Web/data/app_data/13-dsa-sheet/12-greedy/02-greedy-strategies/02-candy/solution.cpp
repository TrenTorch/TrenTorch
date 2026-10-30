#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long candy(vector<long long> ratings) {
    long long n = ratings.size();
    if (n == 0) return 0;
    long long total = 1;
    long long up = 0;
    long long down = 0;
    long long peak = 0;
    for (long long i = 1; i < n; i++) {
        if (ratings[i] > ratings[i - 1]) {
            up++;
            down = 0;
            peak = up;
            total += 1 + up;
        } else if (ratings[i] == ratings[i - 1]) {
            up = 0;
            down = 0;
            peak = 0;
            total += 1;
        } else {
            up = 0;
            down++;
            total += 1 + down;
            if (peak >= down) total--;
        }
    }
    return total;
}

int main() {
    cout << candy(vector<long long>{1, 0, 2}) << endl;
    return 0;
}
