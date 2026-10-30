#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(P log P + L * (log P + 3 * L)) time, O(P) extra space (P products, L search length)
vector<vector<string>> suggestedProducts(vector<string> products, string searchWord) {
    sort(products.begin(), products.end());
    vector<vector<string>> out;
    for (size_t i = 1; i <= searchWord.size(); i++) {
        string prefix = searchWord.substr(0, i);
        size_t start = lower_bound(products.begin(), products.end(), prefix) - products.begin();
        vector<string> row;
        size_t stop = min(products.size(), start + 3);
        for (size_t k = start; k < stop; k++) {
            if (products[k].compare(0, prefix.size(), prefix) == 0) row.push_back(products[k]);
        }
        out.push_back(row);
    }
    return out;
}

int main() {
    cout << suggestedProducts(vector<string>{"mobile", "mouse", "moneypot", "monitor", "mousepad"}, "mouse") << endl;
    return 0;
}
