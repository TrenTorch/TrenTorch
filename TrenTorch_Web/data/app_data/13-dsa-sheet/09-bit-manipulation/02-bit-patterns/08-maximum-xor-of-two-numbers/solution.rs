use std::collections::HashSet;

// O(n) time, O(n) space (30 bits constant)
fn max_xor_pair(nums: Vec<i64>) -> i64 {
    let mut best = 0;
    for bit in (0..30).rev() {
        let prefixes: HashSet<i64> = nums.iter().map(|&x| x >> bit).collect();
        let candidate = (best << 1) | 1;
        best <<= 1;
        for &p in &prefixes {
            if prefixes.contains(&(p ^ candidate)) {
                best = candidate;
                break;
            }
        }
    }
    best
}

fn main() {
    println!("{:?}", max_xor_pair(vec![3, 10, 5, 25, 2, 8]));
}
