class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

// O(n) time, O(1) space
function removeElements(head, val) {
  const dummy = new ListNode(0, head);
  let prev = dummy;
  let cur = head;
  while (cur) {
    if (cur.val === val) {
      prev.next = cur.next;
    } else {
      prev = cur;
    }
    cur = cur.next;
  }
  return dummy.next;
}

// Call removeElements(...) here and console.log the result to try it.
