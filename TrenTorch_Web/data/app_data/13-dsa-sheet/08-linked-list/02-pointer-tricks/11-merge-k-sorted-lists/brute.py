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


def merge_k_lists(lists):
    values = []
    for node in lists:
        values.extend(to_list(node))
    return from_list(sorted(values))
