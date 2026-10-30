#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n log d) time, O(n) space (d = distinct values; the ordered map keeps ties on the smaller value)
vector<long long> frequencyExtremes(vector<long long> nums) {
    map<long long, long long> counts;
    for (long long x : nums) counts[x]++;
    long long most = 0, least = 0, mostCount = -1, leastCount = -1;
    for (const auto& [value, count] : counts) {
        if (mostCount < 0 || count > mostCount) {
            most = value;
            mostCount = count;
        }
        if (leastCount < 0 || count < leastCount) {
            least = value;
            leastCount = count;
        }
    }
    return {most, least};
}

int main() {
    cout << frequencyExtremes(vector<long long>{4, 4, 5, 5, 6}) << endl;
    return 0;
}
