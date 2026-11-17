class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

// O(n) time, O(1) space
function removeAllDuplicates(head) {
  const dummy = new ListNode(0, head);
  let prev = dummy;
  let cur = head;
  while (cur) {
    if (cur.next && cur.next.val === cur.val) {
      const value = cur.val;
      while (cur && cur.val === value) {
        cur = cur.next;
      }
      prev.next = cur;
    } else {
      prev = cur;
      cur = cur.next;
    }
  }
  return dummy.next;
}

// Call removeAllDuplicates(...) here and console.log the result to try it.
function arrayToList(arr) {
  let dummy = new ListNode();
  let cur = dummy;
  for (const val of arr) {
    cur.next = new ListNode(val);
    cur = cur.next;
  }
  return dummy.next;
}

function listToArray(head) {
  const res = [];
  while (head) {
    res.push(head.val);
    head = head.next;
  }
  return res;
}

// Example 1
let head1 = arrayToList([1, 2, 3, 3, 4, 4, 5]);
console.log(listToArray(removeAllDuplicates(head1))); // [1, 2, 5]

// Example 2
let head2 = arrayToList([1, 1, 1, 2, 3]);
console.log(listToArray(removeAllDuplicates(head2))); // [2, 3]

// Edge cases
console.log(listToArray(removeAllDuplicates(arrayToList([])))); // []
console.log(listToArray(removeAllDuplicates(arrayToList([1])))); // [1]
console.log(listToArray(removeAllDuplicates(arrayToList([1, 1])))); // []
console.log(listToArray(removeAllDuplicates(arrayToList([1, 2, 2])))); // [1]
