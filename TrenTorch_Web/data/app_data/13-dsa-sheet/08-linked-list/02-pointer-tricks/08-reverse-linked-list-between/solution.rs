#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) space
fn reverse_between(head: Option<Box<ListNode>>, left: i64, size: i64) -> Option<Box<ListNode>> {
    let mut dummy = Box::new(ListNode { val: 0, next: head });
    let mut prev: &mut Box<ListNode> = &mut dummy;
    for _ in 0..(left - 1) {
        prev = prev.next.as_mut().unwrap();
    }
    // detach the sublist, reversing its first `size` nodes as we go
    let mut current = prev.next.take();
    let mut reversed: Option<Box<ListNode>> = None;
    for _ in 0..size {
        let mut node = current.take().unwrap();
        current = node.next.take();
        node.next = reversed;
        reversed = Some(node);
    }
    // attach the rest of the list to the end of the reversed sublist
    let mut tail: &mut Option<Box<ListNode>> = &mut reversed;
    while tail.is_some() {
        tail = &mut tail.as_mut().unwrap().next;
    }
    *tail = current;
    prev.next = reversed;
    dummy.next
}

fn main() {
    // Call it here and print the result to try it.
}
