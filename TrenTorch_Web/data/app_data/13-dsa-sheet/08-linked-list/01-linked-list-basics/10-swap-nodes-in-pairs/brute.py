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


def swap_pairs(head):
    values = to_list(head)
    for i in range(0, len(values) - 1, 2):
        values[i], values[i + 1] = values[i + 1], values[i]
    return from_list(values)
