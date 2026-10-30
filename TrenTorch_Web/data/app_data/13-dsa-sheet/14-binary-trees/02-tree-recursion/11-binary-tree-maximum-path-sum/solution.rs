#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

fn gain(node: &Option<Box<TreeNode>>, best: &mut i64) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let left = std::cmp::max(0, gain(&n.left, best));
            let right = std::cmp::max(0, gain(&n.right, best));
            *best = std::cmp::max(*best, n.val + left + right);
            n.val + std::cmp::max(left, right)
        }
    }
}

// O(n) time, O(h) space
fn max_path_sum(root: Option<Box<TreeNode>>) -> i64 {
    let mut best = match root.as_ref() {
        Some(node) => node.val,
        None => return 0,
    };
    gain(&root, &mut best);
    best
}

fn main() {
    // Call it here and print the result to try it.
}
