use std::collections::HashSet;

// O(n) expected time, O(n) space
fn longest_consecutive(nums: Vec<i64>) -> i64 {
    let values: HashSet<i64> = nums.into_iter().collect();
    let mut best: i64 = 0;
    for &x in &values {
        if !values.contains(&(x - 1)) {
            let mut length: i64 = 1;
            while values.contains(&(x + length)) {
                length += 1;
            }
            best = best.max(length);
        }
    }
    best
}

fn main() {
    println!("{:?}", longest_consecutive(vec![100, 4, 200, 1, 3, 2]));
}
