#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) extra space
fn remove_elements(head: Option<Box<ListNode>>, val: i64) -> Option<Box<ListNode>> {
    let mut dummy = Box::new(ListNode { val: 0, next: head });
    let mut prev: &mut ListNode = &mut dummy;
    while prev.next.is_some() {
        if prev.next.as_ref().map_or(false, |n| n.val == val) {
            let removed = *prev.next.take().unwrap();
            prev.next = removed.next;
        } else {
            prev = prev.next.as_deref_mut().unwrap();
        }
    }
    let root = *dummy;
    root.next
}

fn main() {
    // Call it here and print the result to try it.
}
