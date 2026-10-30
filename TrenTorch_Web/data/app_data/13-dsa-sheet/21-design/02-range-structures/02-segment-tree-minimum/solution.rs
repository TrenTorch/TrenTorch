// O(n) build, O(log n) per operation, O(n) space (bottom-up segment tree)
fn run_segment_tree(nums: Vec<i64>, ops: Vec<String>) -> Vec<i64> {
    let n = nums.len();
    let inf = i64::MAX;
    let mut tree: Vec<i64> = vec![inf; n];
    tree.extend_from_slice(&nums);
    for i in (1..n).rev() {
        tree[i] = std::cmp::min(tree[2 * i], tree[2 * i + 1]);
    }

    let mut out: Vec<i64> = Vec::new();
    for op in ops.iter() {
        let parts: Vec<&str> = op.split_whitespace().collect();
        if parts[0] == "set" {
            let mut i: usize = parts[1].parse::<usize>().unwrap() + n;
            tree[i] = parts[2].parse::<i64>().unwrap();
            i /= 2;
            while i >= 1 {
                tree[i] = std::cmp::min(tree[2 * i], tree[2 * i + 1]);
                i /= 2;
            }
        } else {
            let l: usize = parts[1].parse().unwrap();
            let r: usize = parts[2].parse().unwrap();
            let mut lo = l + n;
            let mut hi = r + n + 1;
            let mut best = inf;
            while lo < hi {
                if lo & 1 == 1 {
                    best = std::cmp::min(best, tree[lo]);
                    lo += 1;
                }
                if hi & 1 == 1 {
                    hi -= 1;
                    best = std::cmp::min(best, tree[hi]);
                }
                lo /= 2;
                hi /= 2;
            }
            out.push(best);
        }
    }
    out
}

fn main() {
    println!("{:?}", run_segment_tree(vec![5, 2, 8, 1], vec![String::from("min 0 3"), String::from("set 3 9"), String::from("min 0 3"), String::from("min 2 3")]));
}
