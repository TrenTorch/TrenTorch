use std::collections::HashMap;

// O(n) time, O(k) space
fn subarrays_divisible_by_k(nums: Vec<i64>, k: i64) -> i64 {
    let mut seen: HashMap<i64, i64> = HashMap::new();
    seen.insert(0, 1);
    let mut prefix: i64 = 0;
    let mut count: i64 = 0;
    for x in nums {
        prefix = (prefix + x) % k;
        if prefix < 0 {
            prefix += k;
        }
        if let Some(v) = seen.get(&prefix) {
            count += *v;
        }
        let entry = seen.entry(prefix).or_insert(0);
        *entry += 1;
    }
    count
}

fn main() {
    println!("{:?}", subarrays_divisible_by_k(vec![4, 5, 0, -2, -3, 1], 5));
}
