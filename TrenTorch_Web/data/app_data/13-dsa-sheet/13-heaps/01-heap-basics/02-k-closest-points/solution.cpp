#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) average time, O(n) space (randomized quickselect, then sort of the k chosen)
vector<vector<long long>> kClosest(vector<vector<long long>> points, long long k) {
    if (k <= 0) return {};
    using Item = tuple<long long, long long, long long>;  // (squared distance, x, y)
    vector<Item> pool;
    pool.reserve(points.size());
    for (auto& p : points) pool.emplace_back(p[0] * p[0] + p[1] * p[1], p[0], p[1]);
    if (k < (long long)pool.size()) {
        static mt19937 rng(12345);
        vector<Item> chosen;
        long long need = k;
        while (need > 0) {
            uniform_int_distribution<size_t> pick(0, pool.size() - 1);
            Item pivot = pool[pick(rng)];
            vector<Item> less, equal, greater_items;
            for (const Item& item : pool) {
                if (item < pivot) less.push_back(item);
                else if (item == pivot) equal.push_back(item);
                else greater_items.push_back(item);
            }
            long long nl = (long long)less.size();
            long long ne = (long long)equal.size();
            if (need <= nl) {
                pool = less;
            } else if (need <= nl + ne) {
                chosen.insert(chosen.end(), less.begin(), less.end());
                chosen.insert(chosen.end(), equal.begin(), equal.begin() + (need - nl));
                need = 0;
            } else {
                chosen.insert(chosen.end(), less.begin(), less.end());
                chosen.insert(chosen.end(), equal.begin(), equal.end());
                need -= nl + ne;
                pool = greater_items;
            }
        }
        pool = chosen;
    }
    sort(pool.begin(), pool.end());
    vector<vector<long long>> out;
    for (const Item& it : pool) out.push_back({get<1>(it), get<2>(it)});
    return out;
}

int main() {
    cout << kClosest(vector<vector<long long>>{vector<long long>{1, 3}, vector<long long>{-2, 2}}, 1) << endl;
    return 0;
}
