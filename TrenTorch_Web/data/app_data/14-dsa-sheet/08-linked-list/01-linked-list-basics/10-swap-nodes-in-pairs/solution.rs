#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) space
fn swap_pairs(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut dummy = Box::new(ListNode { val: 0, next: head });
    let mut prev: &mut Box<ListNode> = &mut dummy;
    while prev.next.is_some() && prev.next.as_ref().unwrap().next.is_some() {
        let mut a = prev.next.take().unwrap();
        let mut b = a.next.take().unwrap();
        a.next = b.next.take();
        b.next = Some(a);
        prev.next = Some(b);
        prev = prev.next.as_mut().unwrap().next.as_mut().unwrap();
    }
    dummy.next
}

fn main() {
    // Call it here and print the result to try it.
}
