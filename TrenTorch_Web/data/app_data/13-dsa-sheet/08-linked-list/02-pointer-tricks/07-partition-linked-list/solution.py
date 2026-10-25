class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def partition_list(head, x):
    small_dummy, large_dummy = ListNode(), ListNode()
    small_tail, large_tail = small_dummy, large_dummy
    while head:
        if head.val < x:
            small_tail.next = head
            small_tail = head
        else:
            large_tail.next = head
            large_tail = head
        head = head.next
    large_tail.next = None
    small_tail.next = large_dummy.next
    return small_dummy.next
