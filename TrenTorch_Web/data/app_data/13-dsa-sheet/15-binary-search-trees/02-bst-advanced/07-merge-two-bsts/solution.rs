#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

fn inorder(root: Option<&TreeNode>) -> Vec<i64> {
    let mut out: Vec<i64> = Vec::new();
    let mut stack: Vec<&TreeNode> = Vec::new();
    let mut node = root;
    while node.is_some() || !stack.is_empty() {
        while let Some(n) = node {
            stack.push(n);
            node = n.left.as_deref();
        }
        let n = stack.pop().unwrap();
        out.push(n.val);
        node = n.right.as_deref();
    }
    out
}

// O(n + m) time, O(n + m) space
fn merge_bsts(root1: Option<Box<TreeNode>>, root2: Option<Box<TreeNode>>) -> Vec<i64> {
    let a = inorder(root1.as_deref());
    let b = inorder(root2.as_deref());
    let mut out: Vec<i64> = Vec::with_capacity(a.len() + b.len());
    let (mut i, mut j) = (0usize, 0usize);
    while i < a.len() && j < b.len() {
        if a[i] <= b[j] {
            out.push(a[i]);
            i += 1;
        } else {
            out.push(b[j]);
            j += 1;
        }
    }
    out.extend_from_slice(&a[i..]);
    out.extend_from_slice(&b[j..]);
    out
}

fn main() {
    // Call it here and print the result to try it.
}
