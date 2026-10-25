class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    """Merge all the sorted lists into one sorted list."""
    # This is correct but too slow: it merges the lists into the result one after another,
    # so the growing result is walked again for every list.
    result = None
    for node in lists:
        dummy = ListNode()
        tail = dummy
        a, b = result, node
        while a and b:
            if a.val <= b.val:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next
        tail.next = a or b
        result = dummy.next
    return result
