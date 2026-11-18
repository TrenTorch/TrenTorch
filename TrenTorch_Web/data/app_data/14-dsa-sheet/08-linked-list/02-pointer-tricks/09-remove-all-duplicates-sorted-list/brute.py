from collections import Counter


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


def remove_all_duplicates(head):
    values = to_list(head)
    counts = Counter(values)
    return from_list([v for v in values if counts[v] == 1])
