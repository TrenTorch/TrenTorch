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


def intersection_node(list_a, list_b):
    seen = set()
    node = list_a
    while node:
        seen.add(id(node))
        node = node.next
    node = list_b
    while node:
        if id(node) in seen:
            return node
        node = node.next
    return None
