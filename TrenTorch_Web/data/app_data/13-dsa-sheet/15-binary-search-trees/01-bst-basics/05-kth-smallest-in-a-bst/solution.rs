#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(h) space
fn kth_smallest_bst(root: Option<Box<TreeNode>>, k: i64) -> i64 {
    let mut stack = Vec::new();
    let mut current = root.as_deref();
    let mut k = k;

    while current.is_some() || !stack.is_empty() {
        while let Some(node) = current {
            stack.push(node);
            current = node.left.as_deref();
        }
        let node = stack.pop().unwrap();
        k -= 1;
        if k == 0 {
            return node.val;
        }
        current = node.right.as_deref();
    }
    0 // unreachable if k is valid
}

fn main() {
    // Call it here and print the result to try it.
}
