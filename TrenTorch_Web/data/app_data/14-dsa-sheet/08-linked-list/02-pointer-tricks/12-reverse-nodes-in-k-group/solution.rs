#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) space
fn reverse_k_group(head: Option<Box<ListNode>>, k: i64) -> Option<Box<ListNode>> {
    let mut dummy = Box::new(ListNode { val: 0, next: head });
    let mut group_prev: &mut Box<ListNode> = &mut dummy;
    loop {
        // is there a full group of k nodes starting at group_prev.next?
        let has_k = {
            let mut probe = group_prev.next.as_deref();
            for _ in 1..k {
                probe = probe.and_then(|n| n.next.as_deref());
            }
            probe.is_some()
        };
        if !has_k {
            break;
        }
        let mut current = group_prev.next.take();
        let mut reversed: Option<Box<ListNode>> = None;
        for _ in 0..k {
            let mut node = current.take().unwrap();
            current = node.next.take();
            node.next = reversed;
            reversed = Some(node);
        }
        group_prev.next = reversed;
        // walk to the last node of the reversed group (the old first node)
        let mut tail: &mut Box<ListNode> = group_prev.next.as_mut().unwrap();
        for _ in 1..k {
            tail = tail.next.as_mut().unwrap();
        }
        tail.next = current;
        group_prev = tail;
    }
    dummy.next
}

fn main() {
    // Call it here and print the result to try it.
}
