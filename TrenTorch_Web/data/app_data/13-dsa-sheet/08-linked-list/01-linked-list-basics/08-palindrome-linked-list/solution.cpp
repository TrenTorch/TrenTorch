#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

// O(n) time, O(1) extra space (reverses the second half in place, as the Python version does)
bool isPalindromeList(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    ListNode* prev = nullptr;
    while (slow) {
        ListNode* after = slow->next;
        slow->next = prev;
        prev = slow;
        slow = after;
    }
    ListNode* left = head;
    ListNode* right = prev;
    while (right) {
        if (left->val != right->val) return false;
        left = left->next;
        right = right->next;
    }
    return true;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
