#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space (sorted copy of points)
long long minArrows(vector<vector<long long>> points) {
    stable_sort(points.begin(), points.end(), [](const vector<long long>& a, const vector<long long>& b) {
        return a[1] < b[1];
    });
    long long arrows = 0;
    bool hasArrow = false;
    long long arrow = 0;
    for (const auto& p : points) {
        long long start = p[0];
        long long end = p[1];
        if (!hasArrow || start > arrow) {
            arrows++;
            hasArrow = true;
            arrow = end;
        }
    }
    return arrows;
}

int main() {
    cout << minArrows(vector<vector<long long>>{vector<long long>{10, 16}, vector<long long>{2, 8}, vector<long long>{1, 6}, vector<long long>{7, 12}}) << endl;
    return 0;
}
