class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def to_list(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    return values


def from_list(values):
    head = None
    for value in reversed(values):
        head = ListNode(value, head)
    return head


def reorder_list(head):
    values = to_list(head)
    out = []
    left, right = 0, len(values) - 1
    while left <= right:
        out.append(values[left])
        if left != right:
            out.append(values[right])
        left += 1
        right -= 1
    return from_list(out)
