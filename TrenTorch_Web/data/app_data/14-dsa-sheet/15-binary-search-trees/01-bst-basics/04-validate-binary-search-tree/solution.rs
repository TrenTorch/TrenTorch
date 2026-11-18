#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(h) space (where h is tree height, up to 800)
fn is_valid_bst(root: Option<Box<TreeNode>>) -> bool {
    fn check(node: &Option<Box<TreeNode>>, low: i64, high: i64) -> bool {
        match node {
            None => true,
            Some(n) => {
                if !(low < n.val && n.val < high) {
                    return false;
                }
                check(&n.left, low, n.val) && check(&n.right, n.val, high)
            }
        }
    }
    check(&root, i64::MIN, i64::MAX)
}

fn main() {
    // Call it here and print the result to try it.
}
