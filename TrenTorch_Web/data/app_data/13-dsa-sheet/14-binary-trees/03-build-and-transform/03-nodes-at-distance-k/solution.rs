use std::collections::VecDeque;

#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(n) space
fn distance_k(root: Option<Box<TreeNode>>, target: i64, k: i64) -> Vec<i64> {
    // Flatten the tree into an index arena. adj[id] holds the neighbours of
    // node id (its children and its parent), the same graph the Python walks.
    let mut vals: Vec<i64> = Vec::new();
    let mut adj: Vec<Vec<usize>> = Vec::new();
    let mut start: Option<usize> = None;
    let mut stack: Vec<(&TreeNode, Option<usize>)> = Vec::new();
    if let Some(r) = root.as_deref() {
        stack.push((r, None));
    }
    while let Some((node, par)) = stack.pop() {
        let id = vals.len();
        vals.push(node.val);
        adj.push(Vec::new());
        if let Some(p) = par {
            adj[id].push(p);
            adj[p].push(id);
        }
        if node.val == target {
            start = Some(id);
        }
        if let Some(left) = node.left.as_deref() {
            stack.push((left, Some(id)));
        }
        if let Some(right) = node.right.as_deref() {
            stack.push((right, Some(id)));
        }
    }

    let start = start.expect("target value must exist in the tree");
    let mut seen = vec![false; vals.len()];
    seen[start] = true;
    let mut frontier: VecDeque<usize> = VecDeque::new();
    frontier.push_back(start);
    for _ in 0..k {
        for _ in 0..frontier.len() {
            let node = frontier.pop_front().unwrap();
            for &nxt in &adj[node] {
                if !seen[nxt] {
                    seen[nxt] = true;
                    frontier.push_back(nxt);
                }
            }
        }
    }
    let mut out: Vec<i64> = frontier.iter().map(|&id| vals[id]).collect();
    out.sort();
    out
}

fn main() {
    // Call it here and print the result to try it.
}
