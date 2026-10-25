class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def remove_all_duplicates(head):
    dummy = ListNode(0, head)
    prev, cur = dummy, head
    while cur:
        if cur.next and cur.next.val == cur.val:
            value = cur.val
            while cur and cur.val == value:
                cur = cur.next
            prev.next = cur
        else:
            prev = cur
            cur = cur.next
    return dummy.next
