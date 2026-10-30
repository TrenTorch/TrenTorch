#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(h) space (h = tree height, recursion depth)
fn postorder_traversal(root: Option<Box<TreeNode>>) -> Vec<i64> {
    fn walk(node: &Option<Box<TreeNode>>, out: &mut Vec<i64>) {
        if let Some(n) = node {
            walk(&n.left, out);
            walk(&n.right, out);
            out.push(n.val);
        }
    }
    let mut out: Vec<i64> = Vec::new();
    walk(&root, &mut out);
    out
}

fn main() {
    // Call it here and print the result to try it.
}
