class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

// O(n) time, O(1) extra space
function cycleLength(head) {
  // If input is an object with values array and cycle index, build the linked list
  if (head && typeof head === 'object' && Array.isArray(head.values)) {
    const vals = head.values;
    const k = head.cycle;
    if (vals.length === 0) return 0;
    const nodes = vals.map(v => new ListNode(v));
    for (let i = 0; i < nodes.length - 1; i++) {
      nodes[i].next = nodes[i + 1];
    }
    if (k >= 0 && k < nodes.length) {
      nodes[nodes.length - 1].next = nodes[k];
    }
    head = nodes[0];
  }

  let slow = head;
  let fast = head;
  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow === fast) {
      let length = 1;
      let node = slow.next;
      while (node !== slow) {
        node = node.next;
        length += 1;
      }
      return length;
    }
  }
  return 0;
}

// Example usage (you can replace this with your own test cases):
// const input = { values: [3, 2, 0, -4], cycle: 1 };
// console.log(cycleLength(input)); // Expected output: 3

// const input2 = { values: [1, 2], cycle: -1 };
// console.log(cycleLength(input2)); // Expected output: 0
