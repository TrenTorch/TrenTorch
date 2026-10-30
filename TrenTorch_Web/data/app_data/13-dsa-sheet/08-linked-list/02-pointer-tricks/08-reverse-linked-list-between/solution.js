class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

// O(n) time, O(1) space
function reverseBetween(head, left, size) {
  const dummy = new ListNode(0, head);
  let prev = dummy;
  for (let i = 0; i < left - 1; i++) {
    prev = prev.next;
  }
  let cur = prev.next;
  for (let i = 0; i < size - 1; i++) {
    const nxt = cur.next;
    cur.next = nxt.next;
    nxt.next = prev.next;
    prev.next = nxt;
  }
  return dummy.next;
}

// Call reverseBetween(...) here and console.log the result to try it.
