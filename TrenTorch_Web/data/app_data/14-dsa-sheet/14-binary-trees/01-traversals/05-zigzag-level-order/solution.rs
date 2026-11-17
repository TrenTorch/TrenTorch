use std::collections::VecDeque;

#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(w) space (w = widest level)
fn zigzag_level_order(root: Option<Box<TreeNode>>) -> Vec<Vec<i64>> {
    let mut out: Vec<Vec<i64>> = Vec::new();
    let mut queue: VecDeque<&TreeNode> = VecDeque::new();
    if let Some(r) = root.as_deref() {
        queue.push_back(r);
    }
    let mut left_to_right = true;
    while !queue.is_empty() {
        let mut level: Vec<i64> = Vec::new();
        for _ in 0..queue.len() {
            let node = queue.pop_front().unwrap();
            level.push(node.val);
            if let Some(l) = node.left.as_deref() {
                queue.push_back(l);
            }
            if let Some(r) = node.right.as_deref() {
                queue.push_back(r);
            }
        }
        if !left_to_right {
            level.reverse();
        }
        out.push(level);
        left_to_right = !left_to_right;
    }
    out
}

fn main() {
    // Call it here and print the result to try it.
}
