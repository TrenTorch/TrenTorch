class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

// O(n) time, O(1) extra space
function reverseKGroup(head, k) {
  const dummy = new ListNode(0, head);
  let groupPrev = dummy;
  while (true) {
    // find the k-th node from groupPrev
    let kth = groupPrev;
    for (let i = 0; i < k; i++) {
      kth = kth.next;
      if (!kth) {
        return dummy.next;
      }
    }
    const groupNext = kth.next;
    // reverse the group
    let prev = groupNext;
    let cur = groupPrev.next;
    while (cur !== groupNext) {
      const after = cur.next;
      cur.next = prev;
      prev = cur;
      cur = after;
    }
    // reconnect reversed group with the previous part
    const first = groupPrev.next;
    groupPrev.next = kth;
    groupPrev = first;
  }
}

// Call reverseKGroup(...) here and console.log the result to try it.
