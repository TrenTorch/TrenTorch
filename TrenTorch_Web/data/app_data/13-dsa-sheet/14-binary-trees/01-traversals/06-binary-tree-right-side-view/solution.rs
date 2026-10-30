use std::collections::VecDeque;

#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(n) space
fn right_side_view(root: Option<Box<TreeNode>>) -> Vec<i64> {
    let mut result = Vec::new();
    let mut queue = VecDeque::new();
    if let Some(node) = root {
        queue.push_back(node);
    }
    while !queue.is_empty() {
        let level_size = queue.len();
        let mut last_val = 0;
        for _ in 0..level_size {
            if let Some(mut node) = queue.pop_front() {
                last_val = node.val;
                if let Some(left) = node.left.take() {
                    queue.push_back(left);
                }
                if let Some(right) = node.right.take() {
                    queue.push_back(right);
                }
            }
        }
        result.push(last_val);
    }
    result
}

fn main() {
    // Call it here and print the result to try it.
}
