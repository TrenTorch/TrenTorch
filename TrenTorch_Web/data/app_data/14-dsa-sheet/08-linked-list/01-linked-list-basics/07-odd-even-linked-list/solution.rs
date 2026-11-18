#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) extra space (nodes are moved, not copied)
fn odd_even_list(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut odd_chain: Option<Box<ListNode>> = None;
    let mut even_chain: Option<Box<ListNode>> = None;
    let mut odd_tail: &mut Option<Box<ListNode>> = &mut odd_chain;
    let mut even_tail: &mut Option<Box<ListNode>> = &mut even_chain;
    let mut cur = head;
    let mut is_odd = true;
    while let Some(mut node) = cur {
        cur = node.next.take();
        if is_odd {
            *odd_tail = Some(node);
            odd_tail = &mut odd_tail.as_mut().unwrap().next;
        } else {
            *even_tail = Some(node);
            even_tail = &mut even_tail.as_mut().unwrap().next;
        }
        is_odd = !is_odd;
    }
    *odd_tail = even_chain;
    odd_chain
}

fn main() {
    // Call it here and print the result to try it.
}
