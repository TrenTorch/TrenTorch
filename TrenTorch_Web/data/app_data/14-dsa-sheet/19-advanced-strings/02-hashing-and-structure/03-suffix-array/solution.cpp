#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n log n) time, O(n) space (prefix doubling with counting sort)
vector<long long> suffixArray(string s) {
    if (s.empty()) return {};
    long long n0 = s.size();
    vector<long long> text(n0 + 1);
    for (long long i = 0; i < n0; i++) text[i] = (unsigned char)s[i] + 1;
    text[n0] = 0;  // sentinel, smaller than every letter
    long long n = n0 + 1;
    long long maxv = *max_element(text.begin(), text.end());
    long long size = max(maxv + 1, n);

    vector<long long> order(n, 0), cls(n, 0), cntv(size, 0);
    for (long long v : text) cntv[v]++;
    for (long long i = 1; i < size; i++) cntv[i] += cntv[i - 1];
    for (long long i = n - 1; i >= 0; i--) {
        cntv[text[i]]--;
        order[cntv[text[i]]] = i;
    }
    long long classes = 1;
    for (long long i = 1; i < n; i++) {
        if (text[order[i]] != text[order[i - 1]]) classes++;
        cls[order[i]] = classes - 1;
    }

    long long shift = 1;
    while (shift < n) {
        vector<long long> by_second(n);
        for (long long i = 0; i < n; i++) by_second[i] = ((order[i] - shift) % n + n) % n;

        vector<long long> cnt(classes, 0);
        for (long long i = 0; i < n; i++) cnt[cls[by_second[i]]]++;
        for (long long i = 1; i < classes; i++) cnt[i] += cnt[i - 1];
        for (long long i = n - 1; i >= 0; i--) {
            long long c = cls[by_second[i]];
            cnt[c]--;
            order[cnt[c]] = by_second[i];
        }

        vector<long long> new_cls(n, 0);
        classes = 1;
        for (long long i = 1; i < n; i++) {
            long long a = order[i], b = order[i - 1];
            if (cls[a] != cls[b] || cls[(a + shift) % n] != cls[(b + shift) % n]) classes++;
            new_cls[a] = classes - 1;
        }
        new_cls[order[0]] = 0;
        cls = new_cls;
        shift *= 2;
    }
    return vector<long long>(order.begin() + 1, order.end());
}

int main() {
    cout << suffixArray("banana") << endl;
    return 0;
}
