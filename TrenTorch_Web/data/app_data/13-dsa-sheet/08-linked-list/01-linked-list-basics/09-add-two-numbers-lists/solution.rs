#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(max(n, m)) time, O(1) extra space beyond the output list
fn add_two_numbers(l1: Option<Box<ListNode>>, l2: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut dummy: Option<Box<ListNode>> = None;
    let mut tail: &mut Option<Box<ListNode>> = &mut dummy;
    let mut a = l1;
    let mut b = l2;
    let mut carry: i64 = 0;
    while a.is_some() || b.is_some() || carry != 0 {
        let mut total = carry;
        if let Some(node) = a.take() {
            let node = *node;
            total += node.val;
            a = node.next;
        }
        if let Some(node) = b.take() {
            let node = *node;
            total += node.val;
            b = node.next;
        }
        *tail = Some(Box::new(ListNode {
            val: total % 10,
            next: None,
        }));
        tail = &mut tail.as_mut().unwrap().next;
        carry = total / 10;
    }
    dummy
}

fn main() {
    // Call it here and print the result to try it.
}
