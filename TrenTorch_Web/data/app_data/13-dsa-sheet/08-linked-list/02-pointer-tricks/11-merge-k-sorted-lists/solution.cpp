#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

// O(N log k) time, where N is the total number of nodes and k is the number of lists; O(k) space
ListNode* mergeKLists(vector<ListNode*> lists) {
    using Item = tuple<int, int, ListNode*>;
    priority_queue<Item, vector<Item>, greater<Item>> heap;
    for (int i = 0; i < (int)lists.size(); i++) {
        if (lists[i]) heap.push(Item(lists[i]->val, i, lists[i]));
    }
    ListNode dummy;
    ListNode* tail = &dummy;
    while (!heap.empty()) {
        auto [val, i, node] = heap.top();
        heap.pop();
        (void)val;
        tail->next = node;
        tail = node;
        if (node->next) heap.push(Item(node->next->val, i, node->next));
    }
    return dummy.next;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
