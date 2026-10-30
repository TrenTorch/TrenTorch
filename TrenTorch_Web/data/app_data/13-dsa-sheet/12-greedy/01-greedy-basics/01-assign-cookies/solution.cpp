#include <bits/stdc++.h>
using namespace std;

// O(n log n + m log m) time, O(1) extra space (sorting in place)
long long assignCookies(vector<long long> greed, vector<long long> sizes) {
    sort(greed.begin(), greed.end());
    sort(sizes.begin(), sizes.end());
    long long child = 0;
    for (long long cookie : sizes) {
        if (child < (long long)greed.size() && greed[child] <= cookie) child++;
    }
    return child;
}

int main() {
    cout << assignCookies(vector<long long>{1, 2, 3}, vector<long long>{1, 1}) << endl;
    return 0;
}
