#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(min(n, sigma)) space (sigma = alphabet size)
long long longestKDistinct(string s, long long k) {
    map<char, long long> count;
    long long n = s.size();
    long long left = 0;
    long long best = 0;
    for (long long right = 0; right < n; right++) {
        count[s[right]]++;
        while ((long long)count.size() > k) {
            char gone = s[left];
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
    cout << longestKDistinct("eceba", 2) << endl;
    return 0;
}
