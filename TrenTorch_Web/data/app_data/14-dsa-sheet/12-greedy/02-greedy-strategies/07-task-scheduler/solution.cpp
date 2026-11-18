#include <bits/stdc++.h>
using namespace std;

// O(L + k) time where L = len(tasks) and k = distinct tasks, O(k) space
long long leastInterval(string tasks, long long n) {
    if (tasks.empty()) return 0;
    unordered_map<char, long long> counts;
    for (char t : tasks) counts[t]++;
    long long m = 0;
    for (const auto& kv : counts) m = max(m, kv.second);
    long long ties = 0;
    for (const auto& kv : counts) {
        if (kv.second == m) ties++;
    }
    return max((long long)tasks.size(), (m - 1) * (n + 1) + ties);
}

int main() {
    cout << leastInterval("AAABBB", 2) << endl;
    return 0;
}
