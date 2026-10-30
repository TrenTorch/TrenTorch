// O(n log n) time, O(n) space
use std::collections::HashSet;

fn common_values(a: Vec<i64>, b: Vec<i64>) -> Vec<i64> {
    let set_a: HashSet<_> = a.into_iter().collect();
    let set_b: HashSet<_> = b.into_iter().collect();
    let mut result: Vec<_> = set_a.intersection(&set_b).cloned().collect();
    result.sort();
    result
}

fn main() {
    println!("{:?}", common_values(vec![1, 2, 2, 3], vec![2, 2, 3, 4]));
}
