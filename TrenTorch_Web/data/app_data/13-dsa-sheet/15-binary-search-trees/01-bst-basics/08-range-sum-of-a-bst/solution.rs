#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

fn sum_range(node: Option<&TreeNode>, low: i64, high: i64) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            if n.val < low {
                sum_range(n.right.as_deref(), low, high)
            } else if n.val > high {
                sum_range(n.left.as_deref(), low, high)
            } else {
                n.val
                    + sum_range(n.left.as_deref(), low, high)
                    + sum_range(n.right.as_deref(), low, high)
            }
        }
    }
}

// O(n) time, O(h) space where h is the height of the tree
fn range_sum_bst(root: Option<Box<TreeNode>>, low: i64, high: i64) -> i64 {
    sum_range(root.as_deref(), low, high)
}

fn main() {
    // Call it here and print the result to try it.
}
