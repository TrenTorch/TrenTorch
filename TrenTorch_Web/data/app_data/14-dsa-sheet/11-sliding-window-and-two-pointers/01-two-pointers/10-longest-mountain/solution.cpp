#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long longestMountain(vector<long long> arr) {
    long long n = arr.size();
    long long best = 0;
    long long i = 1;
    while (i < n - 1) {
        if (arr[i - 1] < arr[i] && arr[i] > arr[i + 1]) {
            long long left = i - 1;
            while (left > 0 && arr[left - 1] < arr[left]) {
                left--;
            }
            long long right = i + 1;
            while (right < n - 1 && arr[right] > arr[right + 1]) {
                right++;
            }
            best = max(best, right - left + 1);
            i = right + 1;
        } else {
            i++;
        }
    }
    return best;
}

int main() {
    cout << longestMountain(vector<long long>{2, 1, 4, 7, 3, 2, 5}) << endl;
    return 0;
}
