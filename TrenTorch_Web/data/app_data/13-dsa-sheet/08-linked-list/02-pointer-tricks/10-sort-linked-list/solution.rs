#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time per merge level, O(n log n) time overall, O(log n) recursion space
fn merge(a: Option<Box<ListNode>>, b: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut a = a;
    let mut b = b;
    let mut out: Option<Box<ListNode>> = None;
    let mut tail = &mut out;
    loop {
        let take_a = match (a.as_ref(), b.as_ref()) {
            (Some(x), Some(y)) => x.val <= y.val,
            (Some(_), None) => true,
            (None, Some(_)) => false,
            (None, None) => break,
        };
        let node = if take_a {
            let mut n = a.take().unwrap();
            a = n.next.take();
            n
        } else {
            let mut n = b.take().unwrap();
            b = n.next.take();
            n
        };
        *tail = Some(node);
        let last = tail.as_mut().unwrap();
        tail = &mut last.next;
    }
    out
}

// O(n log n) time, O(log n) space
fn sort_list(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    if head.as_ref().map_or(true, |n| n.next.is_none()) {
        return head;
    }
    let mut head = head;
    let mut len = 0usize;
    let mut counter = head.as_deref();
    while let Some(node) = counter {
        len += 1;
        counter = node.next.as_deref();
    }
    let first_len = (len + 1) / 2;
    let mut cursor = head.as_mut().unwrap();
    for _ in 1..first_len {
        cursor = cursor.next.as_mut().unwrap();
    }
    let second = cursor.next.take();
    let first_sorted = sort_list(head);
    let second_sorted = sort_list(second);
    merge(first_sorted, second_sorted)
}

fn main() {
    // Call it here and print the result to try it.
}
