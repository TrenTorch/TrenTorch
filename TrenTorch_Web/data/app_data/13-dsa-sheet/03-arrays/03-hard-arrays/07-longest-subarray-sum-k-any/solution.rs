use std::collections::HashMap;

// O(n) time, O(n) space
fn longest_subarray_sum_k_any(nums: Vec<i64>, k: i64) -> i64 {
    let mut first: HashMap<i64, i64> = HashMap::new();
    first.insert(0, -1);
    let mut prefix: i64 = 0;
    let mut best: i64 = 0;
    for (i, &x) in nums.iter().enumerate() {
        prefix += x;
        if let Some(&start) = first.get(&(prefix - k)) {
            let length = i as i64 - start;
            if length > best {
                best = length;
            }
        }
        first.entry(prefix).or_insert(i as i64);
    }
    best
}

fn main() {
    println!("{:?}", longest_subarray_sum_k_any(vec![1, -1, 5, -2, 3], 3));
}
