#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) space
fn rotate_list(head: Option<Box<ListNode>>, k: i64) -> Option<Box<ListNode>> {
    let mut head = head;
    if head.is_none() || head.as_ref().unwrap().next.is_none() {
        return head;
    }

    // Compute length
    let mut length = 0;
    let mut curr = head.as_ref();
    while let Some(node) = curr {
        length += 1;
        curr = node.next.as_ref();
    }

    let k = (k % length as i64) as usize;
    if k == 0 {
        return head;
    }

    // Find new_tail and split the list
    let mut new_head = None;
    {
        let mut new_tail = head.as_mut().unwrap();
        for _ in 0..length - k - 1 {
            new_tail = new_tail.next.as_mut().unwrap();
        }
        new_head = new_tail.next.take();
    }

    // Find tail of new_head and attach original head
    let mut tail = new_head.as_mut().unwrap();
    while tail.next.is_some() {
        tail = tail.next.as_mut().unwrap();
    }
    tail.next = head;

    new_head
}

fn main() {
    // Call it here and print the result to try it.
}
