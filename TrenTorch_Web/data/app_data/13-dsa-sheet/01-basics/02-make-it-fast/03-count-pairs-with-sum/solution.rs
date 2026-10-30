// O(n) time, O(n) space
fn count_pairs_with_sum(nums: Vec<i64>, target: i64) -> i64 {
    use std::collections::HashMap;
    let mut seen = HashMap::new();
    let mut count = 0;
    for x in nums {
        count += seen.get(&(target - x)).copied().unwrap_or(0);
        *seen.entry(x).or_insert(0) += 1;
    }
    count
}

fn main() {
    println!("{:?}", count_pairs_with_sum(vec![1, 2, 3, 4, 3], 6));
}
