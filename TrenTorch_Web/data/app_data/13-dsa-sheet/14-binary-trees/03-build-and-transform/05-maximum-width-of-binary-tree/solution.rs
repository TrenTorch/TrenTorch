#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(n) space
fn width_of_tree(root: Option<Box<TreeNode>>) -> i64 {
    use std::collections::VecDeque;

    let mut best = 0;
    let mut queue = VecDeque::new();

    if let Some(node) = root {
        queue.push_back((node, 0));
    }

    while !queue.is_empty() {
        let first = queue[0].1;
        let mut last = first;

        for _ in 0..queue.len() {
            if let Some((node, index)) = queue.pop_front() {
                last = index;
                if let Some(left) = node.left {
                    queue.push_back((left, 2 * index + 1));
                }
                if let Some(right) = node.right {
                    queue.push_back((right, 2 * index + 2));
                }
            }
        }

        best = best.max(last - first + 1);
    }

    best
}

fn main() {
    // Call it here and print the result to try it.
}
