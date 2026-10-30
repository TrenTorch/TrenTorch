#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n + m) time, O(1) extra space (nodes are re-linked, not copied)
fn merge_two_lists(list1: Option<Box<ListNode>>, list2: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut dummy: Option<Box<ListNode>> = None;
    let mut tail: &mut Option<Box<ListNode>> = &mut dummy;
    let mut a = list1;
    let mut b = list2;
    loop {
        let take_a = match (&a, &b) {
            (Some(x), Some(y)) => x.val <= y.val,
            (Some(_), None) => true,
            (None, Some(_)) => false,
            (None, None) => break,
        };
        let source = if take_a { &mut a } else { &mut b };
        let mut node = source.take().unwrap();
        *source = node.next.take();
        *tail = Some(node);
        tail = &mut tail.as_mut().unwrap().next;
    }
    dummy
}

fn main() {
    // Call it here and print the result to try it.
}
