class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def cycle_length(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            length = 1
            node = slow.next
            while node is not slow:
                node = node.next
                length += 1
            return length
    return 0
