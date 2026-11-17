#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

// O(n) time, O(1) space
ListNode* reverseBetween(ListNode* head, long long left, long long size) {
    ListNode dummy(0, head);
    ListNode* prev = &dummy;
    for (long long i = 0; i < left - 1; i++) prev = prev->next;
    ListNode* cur = prev->next;
    for (long long i = 0; i < size - 1; i++) {
        ListNode* nxt = cur->next;
        cur->next = nxt->next;
        nxt->next = prev->next;
        prev->next = nxt;
    }
    return dummy.next;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
