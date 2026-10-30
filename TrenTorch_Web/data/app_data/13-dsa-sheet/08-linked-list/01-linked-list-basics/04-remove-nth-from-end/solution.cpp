#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

// O(n) time, O(1) space (single pass with two pointers)
ListNode* removeNthFromEnd(ListNode* head, long long n) {
    ListNode dummy(0, head);
    ListNode* fast = &dummy;
    ListNode* slow = &dummy;
    for (long long i = 0; i < n; i++) fast = fast->next;
    while (fast->next) {
        fast = fast->next;
        slow = slow->next;
    }
    slow->next = slow->next->next;
    return dummy.next;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
