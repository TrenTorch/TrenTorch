#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

// O(m + n) time, O(1) space
ListNode* intersectionNode(ListNode* listA, ListNode* listB) {
    ListNode* pa = listA;
    ListNode* pb = listB;
    while (pa != pb) {
        pa = pa ? pa->next : listB;
        pb = pb ? pb->next : listA;
    }
    return pa;
}

int main() {
    return 0;
}
