class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def remove_elements(head, val):
    dummy = ListNode(0, head)
    prev, cur = dummy, head
    while cur:
        if cur.val == val:
            prev.next = cur.next
        else:
            prev = cur
        cur = cur.next
    return dummy.next
