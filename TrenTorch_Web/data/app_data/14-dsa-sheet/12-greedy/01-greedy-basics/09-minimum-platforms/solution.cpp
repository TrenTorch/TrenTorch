#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space (sorted copies of arrivals and departures)
long long minPlatforms(vector<long long> arrivals, vector<long long> departures) {
    sort(arrivals.begin(), arrivals.end());
    sort(departures.begin(), departures.end());
    size_t i = 0;
    size_t j = 0;
    long long current = 0;
    long long best = 0;
    while (i < arrivals.size()) {
        if (arrivals[i] <= departures[j]) {
            current++;
            best = max(best, current);
            i++;
        } else {
            current--;
            j++;
        }
    }
    return best;
}

int main() {
    cout << minPlatforms(vector<long long>{900, 940, 950, 1100, 1500, 1800}, vector<long long>{910, 1200, 1120, 1130, 1900, 2000}) << endl;
    return 0;
}
