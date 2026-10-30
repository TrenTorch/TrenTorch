use std::collections::HashMap;

// O(n + m) time, O(n) space
fn count_frequencies(nums: Vec<i64>, queries: Vec<i64>) -> Vec<i64> {
    let mut counts = HashMap::with_capacity(nums.len());
    for v in nums {
        *counts.entry(v).or_insert(0) += 1;
    }
    let mut ans = Vec::with_capacity(queries.len());
    for q in queries {
        ans.push(*counts.get(&q).unwrap_or(&0));
    }
    ans
}

fn main() {
    println!("{:?}", count_frequencies(vec![1, 2, 2, 3, 3, 3], vec![3, 2, 5]));
}
