use std::collections::VecDeque;

#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(n) space
fn level_order(root: Option<Box<TreeNode>>) -> Vec<Vec<i64>> {
    let mut out = Vec::new();
    let mut queue = VecDeque::new();
    if let Some(node) = root {
        queue.push_back(node);
    }
    while !queue.is_empty() {
        let level_size = queue.len();
        let mut level = Vec::with_capacity(level_size);
        for _ in 0..level_size {
            let node = queue.pop_front().unwrap();
            level.push(node.val);
            if let Some(left) = node.left {
                queue.push_back(left);
            }
            if let Some(right) = node.right {
                queue.push_back(right);
            }
        }
        out.push(level);
    }
    out
}

fn main() {
    // Call it here and print the result to try it.
}
