#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(h) space where h is the height of the tree
fn trim_bst(root: Option<Box<TreeNode>>, low: i64, high: i64) -> Option<Box<TreeNode>> {
    match root {
        None => None,
        Some(mut node) => {
            if node.val < low {
                return trim_bst(node.right.take(), low, high);
            }
            if node.val > high {
                return trim_bst(node.left.take(), low, high);
            }
            node.left = trim_bst(node.left.take(), low, high);
            node.right = trim_bst(node.right.take(), low, high);
            Some(node)
        }
    }
}

fn main() {
    // Call it here and print the result to try it.
}
