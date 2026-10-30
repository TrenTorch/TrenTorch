#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

// O(n) time, O(1) space
ListNode* reverseKGroup(ListNode* head, long long k) {
    ListNode dummy(0, head);
    ListNode* groupPrev = &dummy;
    while (true) {
        ListNode* kth = groupPrev;
        for (long long i = 0; i < k; i++) {
            kth = kth->next;
            if (!kth) return dummy.next;
        }
        ListNode* groupNext = kth->next;
        ListNode* prev = groupNext;
        ListNode* cur = groupPrev->next;
        while (cur != groupNext) {
            ListNode* after = cur->next;
            cur->next = prev;
            prev = cur;
            cur = after;
        }
        ListNode* first = groupPrev->next;
        groupPrev->next = kth;
        groupPrev = first;
    }
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
