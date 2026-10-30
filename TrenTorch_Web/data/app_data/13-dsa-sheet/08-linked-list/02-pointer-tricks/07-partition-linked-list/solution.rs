#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) extra space
fn partition_list(head: Option<Box<ListNode>>, x: i64) -> Option<Box<ListNode>> {
    let mut small: Option<Box<ListNode>> = None;
    let mut large: Option<Box<ListNode>> = None;
    let mut small_tail: &mut Option<Box<ListNode>> = &mut small;
    let mut large_tail: &mut Option<Box<ListNode>> = &mut large;
    let mut cur = head;
    while let Some(mut node) = cur.take() {
        cur = node.next.take();
        if node.val < x {
            *small_tail = Some(node);
            let last = small_tail.as_mut().unwrap();
            small_tail = &mut last.next;
        } else {
            *large_tail = Some(node);
            let last = large_tail.as_mut().unwrap();
            large_tail = &mut last.next;
        }
    }
    *small_tail = large;
    small
}

fn main() {
    // Call it here and print the result to try it.
}
