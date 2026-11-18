#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n log n) time, O(n) space
fn vertical_order(root: Option<Box<TreeNode>>) -> Vec<Vec<i64>> {
    use std::collections::{HashMap, VecDeque};

    let mut columns: HashMap<i64, Vec<(i64, i64)>> = HashMap::new();
    let mut queue = VecDeque::new();

    if let Some(root) = root {
        queue.push_back((root, 0, 0));
    }

    while let Some((node, row, col)) = queue.pop_front() {
        columns.entry(col).or_default().push((row, node.val));
        if let Some(left) = node.left {
            queue.push_back((left, row + 1, col - 1));
        }
        if let Some(right) = node.right {
            queue.push_back((right, row + 1, col + 1));
        }
    }

    let mut entries: Vec<_> = columns.into_iter().collect();
    entries.sort_by_key(|(col, _)| *col);

    let mut result = Vec::new();
    for (_, mut vec) in entries {
        vec.sort_by(|a, b| a.0.cmp(&b.0).then(a.1.cmp(&b.1)));
        result.push(vec.into_iter().map(|(_, v)| v).collect());
    }

    result
}

fn main() {
    // Call it here and print the result to try it.
}
