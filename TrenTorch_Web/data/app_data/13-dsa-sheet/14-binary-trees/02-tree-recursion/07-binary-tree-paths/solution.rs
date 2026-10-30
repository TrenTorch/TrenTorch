#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

fn go(node: Option<&TreeNode>, path: &mut Vec<String>, out: &mut Vec<String>) {
    let node = match node {
        None => return,
        Some(n) => n,
    };
    path.push(node.val.to_string());
    if node.left.is_none() && node.right.is_none() {
        out.push(path.join("->"));
    } else {
        go(node.left.as_deref(), path, out);
        go(node.right.as_deref(), path, out);
    }
    path.pop();
}

// O(n * h) time for the path strings, O(h) extra space besides the output
fn root_to_leaf_paths(root: Option<Box<TreeNode>>) -> Vec<String> {
    let mut out: Vec<String> = Vec::new();
    let mut path: Vec<String> = Vec::new();
    go(root.as_deref(), &mut path, &mut out);
    out
}

fn main() {
    // Call it here and print the result to try it.
}
