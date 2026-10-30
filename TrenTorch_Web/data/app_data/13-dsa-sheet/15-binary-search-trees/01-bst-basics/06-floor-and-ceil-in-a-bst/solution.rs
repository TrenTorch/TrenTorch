#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(h) time, O(1) extra space where h is the height of the tree
fn floor_and_ceil_bst(root: Option<Box<TreeNode>>, x: i64) -> Vec<i64> {
    let mut floor: i64 = -1;
    let mut ceil: i64 = -1;
    let mut node = root.as_deref();
    while let Some(n) = node {
        if n.val == x {
            return vec![x, x];
        }
        if n.val < x {
            floor = n.val;
            node = n.right.as_deref();
        } else {
            ceil = n.val;
            node = n.left.as_deref();
        }
    }
    vec![floor, ceil]
}

fn main() {
    // Call it here and print the result to try it.
}
