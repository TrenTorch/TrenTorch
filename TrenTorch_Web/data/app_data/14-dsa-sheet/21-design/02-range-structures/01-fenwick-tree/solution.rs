// O((n + q) log n) time, O(n) space (Fenwick tree)
fn run_fenwick(nums: Vec<i64>, ops: Vec<String>) -> Vec<i64> {
    let n = nums.len();
    let mut tree = vec![0i64; n + 1];
    let mut values = nums.clone();

    for (i, &x) in nums.iter().enumerate() {
        fenwick_add(&mut tree, n, i, x);
    }

    let mut out: Vec<i64> = Vec::new();
    for op in ops.iter() {
        let parts: Vec<&str> = op.split_whitespace().collect();
        if parts[0] == "set" {
            let i: usize = parts[1].parse().unwrap();
            let v: i64 = parts[2].parse().unwrap();
            let delta = v - values[i];
            fenwick_add(&mut tree, n, i, delta);
            values[i] = v;
        } else {
            let left: usize = parts[1].parse().unwrap();
            let right: usize = parts[2].parse().unwrap();
            let sum = fenwick_prefix(&tree, right + 1) - fenwick_prefix(&tree, left);
            out.push(sum);
        }
    }
    out
}

fn fenwick_add(tree: &mut [i64], n: usize, i: usize, delta: i64) {
    let mut idx = i + 1;
    while idx <= n {
        tree[idx] += delta;
        idx += idx & idx.wrapping_neg();
    }
}

fn fenwick_prefix(tree: &[i64], mut i: usize) -> i64 {
    let mut total: i64 = 0;
    while i > 0 {
        total += tree[i];
        i -= i & i.wrapping_neg();
    }
    total
}

fn main() {
    println!("{:?}", run_fenwick(vec![1, 2, 3, 4], vec![String::from("sum 0 3"), String::from("set 1 10"), String::from("sum 0 2"), String::from("sum 1 1")]));
}
