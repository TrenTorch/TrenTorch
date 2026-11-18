#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) space
fn reorder_list(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    if head.is_none() || head.as_ref().unwrap().next.is_none() {
        return head;
    }
    let mut head = head;
    let mut len = 0usize;
    let mut counter = head.as_deref();
    while let Some(node) = counter {
        len += 1;
        counter = node.next.as_deref();
    }
    // first half keeps (len + 1) / 2 nodes, same split as the Python slow/fast walk
    let first_len = (len + 1) / 2;
    let mut split = head.as_mut().unwrap();
    for _ in 1..first_len {
        split = split.next.as_mut().unwrap();
    }
    let mut second_cur = split.next.take();

    // reverse the second half
    let mut prev: Option<Box<ListNode>> = None;
    while let Some(mut node) = second_cur.take() {
        second_cur = node.next.take();
        node.next = prev;
        prev = Some(node);
    }

    // interleave first and reversed second half
    let mut first = head;
    let mut second = prev;
    let mut out: Option<Box<ListNode>> = None;
    let mut tail = &mut out;
    while let Some(mut f) = first.take() {
        first = f.next.take();
        *tail = Some(f);
        let node = tail.as_mut().unwrap();
        tail = &mut node.next;
        if let Some(mut s) = second.take() {
            second = s.next.take();
            *tail = Some(s);
            let node = tail.as_mut().unwrap();
            tail = &mut node.next;
        }
    }
    if second.is_some() {
        *tail = second;
    }
    out
}

fn main() {
    // Call it here and print the result to try it.
}
