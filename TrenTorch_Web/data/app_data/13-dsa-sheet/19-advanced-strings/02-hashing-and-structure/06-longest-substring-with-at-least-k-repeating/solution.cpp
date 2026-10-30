#include <bits/stdc++.h>
using namespace std;

// O(26 * n) time, O(n) recursion depth worst case (divide on rare letters), O(sigma) space per level
long long longestSubstringKRepeating(string s, long long k) {
    function<long long(long long, long long)> solve = [&](long long lo, long long hi) -> long long {
        if (hi - lo < k) return 0;
        map<char, long long> counts;
        for (long long i = lo; i < hi; i++) counts[s[i]]++;
        set<char> rare;
        for (const auto& kv : counts) {
            if (kv.second < k) rare.insert(kv.first);
        }
        if (rare.empty()) return hi - lo;
        long long best = 0, start = lo;
        for (long long i = lo; i <= hi; i++) {
            if (i == hi || rare.count(s[i])) {
                best = max(best, solve(start, i));
                start = i + 1;
            }
        }
        return best;
    };
    return solve(0, (long long)s.size());
}

int main() {
    cout << longestSubstringKRepeating("aaabb", 3) << endl;
    return 0;
}
