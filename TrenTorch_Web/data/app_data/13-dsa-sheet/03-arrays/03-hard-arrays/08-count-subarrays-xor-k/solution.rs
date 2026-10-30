// O(n) time, O(n) space
fn count_subarrays_xor_k(nums: Vec<i64>, k: i64) -> i64 {
    use std::collections::HashMap;
    let mut seen: HashMap<i64, i64> = HashMap::new();
    seen.insert(0, 1);
    let mut prefix = 0i64;
    let mut count = 0i64;
    for x in nums {
        prefix ^= x;
        let target = prefix ^ k;
        if let Some(v) = seen.get(&target) {
            count += v;
        }
        *seen.entry(prefix).or_insert(0) += 1;
    }
    count
}

fn main() {
    println!("{:?}", count_subarrays_xor_k(vec![4, 2, 2, 6, 4], 6));
}
