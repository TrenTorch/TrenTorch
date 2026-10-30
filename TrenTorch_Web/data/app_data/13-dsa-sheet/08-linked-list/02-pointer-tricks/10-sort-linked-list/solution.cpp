#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

ListNode* mergeSortedLists(ListNode* a, ListNode* b) {
    ListNode dummy;
    ListNode* tail = &dummy;
    while (a && b) {
        if (a->val <= b->val) {
            tail->next = a;
            a = a->next;
        } else {
            tail->next = b;
            b = b->next;
        }
        tail = tail->next;
    }
    tail->next = a ? a : b;
    return dummy.next;
}

// O(n log n) time, O(log n) space (recursion stack)
ListNode* sortList(ListNode* head) {
    if (!head || !head->next) return head;
    ListNode* slow = head;
    ListNode* fast = head->next;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    ListNode* second = slow->next;
    slow->next = nullptr;
    return mergeSortedLists(sortList(head), sortList(second));
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
