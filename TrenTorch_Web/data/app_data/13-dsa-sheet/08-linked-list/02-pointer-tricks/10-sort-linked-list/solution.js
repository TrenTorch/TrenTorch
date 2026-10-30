class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

// O(n log n) time, O(log n) space
function sortList(head) {
  function merge(a, b) {
    const dummy = new ListNode();
    let tail = dummy;
    while (a && b) {
      if (a.val <= b.val) {
        tail.next = a;
        a = a.next;
      } else {
        tail.next = b;
        b = b.next;
      }
      tail = tail.next;
    }
    tail.next = a || b;
    return dummy.next;
  }

  if (!head || !head.next) {
    return head;
  }
  let slow = head;
  let fast = head.next;
  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
  }
  const second = slow.next;
  slow.next = null;
  return merge(sortList(head), sortList(second));
}

// Call sortList(...) here and console.log the result to try it.
