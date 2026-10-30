#include <bits/stdc++.h>
using namespace std;

// O(items * capacity) time, O(capacity) space
long long unboundedKnapsack(vector<long long> weights, vector<long long> values, long long capacity) {
    vector<long long> best(capacity + 1, 0);
    size_t count = min(weights.size(), values.size());
    for (size_t i = 0; i < count; ++i) {
        long long weight = weights[i], value = values[i];
        for (long long w = weight; w <= capacity; ++w) {
            if (best[w - weight] + value > best[w]) best[w] = best[w - weight] + value;
        }
    }
    return best[capacity];
}

int main() {
    cout << unboundedKnapsack(vector<long long>{1, 3, 4}, vector<long long>{15, 50, 60}, 8) << endl;
    return 0;
}
