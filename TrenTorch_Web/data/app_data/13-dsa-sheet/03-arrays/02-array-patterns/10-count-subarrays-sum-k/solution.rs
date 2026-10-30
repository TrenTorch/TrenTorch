use std::collections::HashMap;

// O(n) time, O(n) space
fn count_subarrays_sum_k(nums: Vec<i64>, k: i64) -> i64 {
    let mut seen: HashMap<i64, i64> = HashMap::new();
    seen.insert(0, 1);
    let mut prefix = 0i64;
    let mut count = 0i64;
    for x in nums {
        prefix += x;
        if let Some(v) = seen.get(&(prefix - k)) {
            count += *v;
        }
        let entry = seen.entry(prefix).or_insert(0);
        *entry += 1;
    }
    count
}

fn main() {
    println!("{:?}", count_subarrays_sum_k(vec![1, 1, 1], 2));
}
