#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long maxPoints(vector<long long> points, long long k) {
    long long n = points.size();
    long long size = n - k;
    long long total = 0;
    for (long long x : points) {
        total += x;
    }
    long long window = 0;
    for (long long i = 0; i < size; i++) {
        window += points[i];
    }
    long long smallest = window;
    for (long long i = size; i < n; i++) {
        window += points[i] - points[i - size];
        smallest = min(smallest, window);
    }
    return total - smallest;
}

int main() {
    cout << maxPoints(vector<long long>{1, 2, 3, 4, 5, 6, 1}, 3) << endl;
    return 0;
}
