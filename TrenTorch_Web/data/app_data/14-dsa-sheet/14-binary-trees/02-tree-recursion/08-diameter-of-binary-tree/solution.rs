#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

fn height(node: &Option<Box<TreeNode>>, best: &mut i64) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let left = height(&n.left, best);
            let right = height(&n.right, best);
            *best = (*best).max(left + right);
            1 + left.max(right)
        }
    }
}

// O(n) time, O(h) space where h is tree height (recursion stack)
fn diameter(root: Option<Box<TreeNode>>) -> i64 {
    let mut best = 0;
    height(&root, &mut best);
    best
}

fn main() {
    // Call it here and print the result to try it.
}
