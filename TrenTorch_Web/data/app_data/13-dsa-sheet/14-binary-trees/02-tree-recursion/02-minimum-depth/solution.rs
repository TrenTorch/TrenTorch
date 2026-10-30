use std::collections::VecDeque;

#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(n) space
fn min_depth(root: Option<Box<TreeNode>>) -> i64 {
    let root = match root {
        None => return 0,
        Some(r) => r,
    };
    let mut queue: VecDeque<(&TreeNode, i64)> = VecDeque::new();
    queue.push_back((&*root, 1));
    while let Some((node, depth)) = queue.pop_front() {
        if node.left.is_none() && node.right.is_none() {
            return depth;
        }
        if let Some(left) = node.left.as_deref() {
            queue.push_back((left, depth + 1));
        }
        if let Some(right) = node.right.as_deref() {
            queue.push_back((right, depth + 1));
        }
    }
    0
}

fn main() {
    // Call it here and print the result to try it.
}
