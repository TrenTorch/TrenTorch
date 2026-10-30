#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(h) space where h is tree height (≤ 800)
fn min_diff_bst(root: Option<Box<TreeNode>>) -> i64 {
    let mut best = i64::MAX;
    let mut prev: Option<i64> = None;
    let mut stack = Vec::new();
    let mut current = root;

    while current.is_some() || !stack.is_empty() {
        while let Some(mut node) = current {
            current = node.left.take();
            stack.push(node);
        }

        if let Some(mut node) = stack.pop() {
            if let Some(p) = prev {
                let diff = node.val - p;
                if diff < best {
                    best = diff;
                }
            }
            prev = Some(node.val);
            current = node.right.take();
        }
    }

    best
}

fn main() {
    // Call it here and print the result to try it.
}
