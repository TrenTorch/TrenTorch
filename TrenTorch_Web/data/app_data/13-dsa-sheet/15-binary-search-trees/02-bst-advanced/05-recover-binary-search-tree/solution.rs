#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// Inorder scan state: (inorder index, value) of the nodes that break the order.
struct Scan {
    idx: usize,
    prev: Option<(usize, i64)>,
    first: Option<(usize, i64)>,
    second: Option<(usize, i64)>,
}

fn scan(node: Option<&TreeNode>, s: &mut Scan) {
    let n = match node {
        None => return,
        Some(n) => n,
    };
    scan(n.left.as_deref(), s);
    let cur = (s.idx, n.val);
    if let Some((_, prev_val)) = s.prev {
        if prev_val > n.val {
            if s.first.is_none() {
                s.first = s.prev;
            }
            s.second = Some(cur);
        }
    }
    s.prev = Some(cur);
    s.idx += 1;
    scan(n.right.as_deref(), s);
}

// Writes the swapped values back at their inorder positions.
fn swap_at(node: Option<&mut TreeNode>, counter: &mut usize, fi: usize, fv: i64, si: usize, sv: i64) {
    if let Some(n) = node {
        swap_at(n.left.as_deref_mut(), counter, fi, fv, si, sv);
        if *counter == fi {
            n.val = sv;
        } else if *counter == si {
            n.val = fv;
        }
        *counter += 1;
        swap_at(n.right.as_deref_mut(), counter, fi, fv, si, sv);
    }
}

// O(n) time, O(h) space where h is the height of the tree
fn recover_tree(mut root: Option<Box<TreeNode>>) -> Option<Box<TreeNode>> {
    let mut s = Scan {
        idx: 0,
        prev: None,
        first: None,
        second: None,
    };
    scan(root.as_deref(), &mut s);
    let (fi, fv) = s.first.expect("two swapped nodes must exist");
    let (si, sv) = s.second.expect("two swapped nodes must exist");
    let mut counter: usize = 0;
    swap_at(root.as_deref_mut(), &mut counter, fi, fv, si, sv);
    root
}

fn main() {
    // Call it here and print the result to try it.
}
