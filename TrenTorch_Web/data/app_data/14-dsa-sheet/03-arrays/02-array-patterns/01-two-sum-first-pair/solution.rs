use std::collections::HashMap;

// O(n) time, O(n) space
fn two_sum_first_pair(nums: Vec<i64>, target: i64) -> Vec<i64> {
    let mut first: HashMap<i64, usize> = HashMap::new();
    let mut best: Option<(usize, usize)> = None;
    for (j, &x) in nums.iter().enumerate() {
        if let Some(&i) = first.get(&(target - x)) {
            if best.map_or(true, |(bi, bj)| (i, j) < (bi, bj)) {
                best = Some((i, j));
            }
        }
        first.entry(x).or_insert(j);
    }
    match best {
        Some((i, j)) => vec![i as i64, j as i64],
        None => vec![-1, -1],
    }
}

fn main() {
    println!("{:?}", two_sum_first_pair(vec![1, 6, 5, 3, 8], 9));
}
