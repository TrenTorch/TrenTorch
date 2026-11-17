#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(h) time, O(1) space where h is the height of the tree.
fn closest_value(root: Option<Box<TreeNode>>, target: i64) -> i64 {
    let mut best = root.as_ref().expect("root is non-empty").val;
    let mut node = root.as_ref();
    while let Some(n) = node {
        let val = n.val;
        let diff_val = (val - target).abs();
        let diff_best = (best - target).abs();
        if (diff_val, val) < (diff_best, best) {
            best = val;
        }
        node = if target < val { n.left.as_ref() } else { n.right.as_ref() };
    }
    best
}

fn main() {
    // Call it here and print the result to try it.
}
