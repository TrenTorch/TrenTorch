// O(n) time, O(n) space
fn longest_zero_sum_subarray(nums: Vec<i64>) -> i64 {
    use std::collections::HashMap;
    let mut first = HashMap::new();
    first.insert(0, -1);
    let mut prefix = 0;
    let mut best = 0;
    for (i, &x) in nums.iter().enumerate() {
        prefix += x;
        let i_i64 = i as i64;
        if let Some(&first_idx) = first.get(&prefix) {
            let len = i_i64 - first_idx;
            if len > best {
                best = len;
            }
        } else {
            first.insert(prefix, i_i64);
        }
    }
    best
}

fn main() {
    println!("{:?}", longest_zero_sum_subarray(vec![15, -2, 2, -8, 1, 7, 10, 23]));
}
