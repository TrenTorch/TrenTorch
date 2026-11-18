#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

// O(n) time, O(1) space
ListNode* reorderList(ListNode* head) {
    if (!head || !head->next) return head;
    ListNode* slow = head;
    ListNode* fast = head->next;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    ListNode* second = slow->next;
    slow->next = nullptr;
    ListNode* prev = nullptr;
    while (second) {
        ListNode* after = second->next;
        second->next = prev;
        prev = second;
        second = after;
    }
    ListNode* first = head;
    second = prev;
    while (second) {
        ListNode* a = first->next;
        ListNode* b = second->next;
        first->next = second;
        second->next = a;
        first = a;
        second = b;
    }
    return head;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
