#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(L) time in one walk of the list (fast pointer n ahead, then slow pointer), O(1) extra space
fn remove_nth_from_end(head: Option<Box<ListNode>>, n: i64) -> Option<Box<ListNode>> {
    let mut dummy = Box::new(ListNode { val: 0, next: head });
    // Fast pointer runs n nodes ahead, then keeps going to the end, counting steps.
    let mut fast: &ListNode = &dummy;
    for _ in 0..n {
        fast = fast.next.as_deref().unwrap();
    }
    let mut steps = 0usize;
    while let Some(next) = fast.next.as_deref() {
        fast = next;
        steps += 1;
    }
    // Slow pointer moves the same number of steps and stops before the target node.
    let mut slow: &mut ListNode = &mut dummy;
    for _ in 0..steps {
        slow = slow.next.as_deref_mut().unwrap();
    }
    if let Some(node) = slow.next.take() {
        let node = *node;
        slow.next = node.next;
    }
    let root = *dummy;
    root.next
}

fn main() {
    // Call it here and print the result to try it.
}
