use std::collections::HashMap;

// O(n * D) time, O(D) space (D = number of distinct running sums, at most 2 * sum(nums) + 1)
fn find_target_sum_ways(nums: Vec<i64>, target: i64) -> i64 {
    let mut ways: HashMap<i64, i64> = HashMap::new();
    ways.insert(0, 1);
    for x in nums {
        let mut next: HashMap<i64, i64> = HashMap::new();
        for (&s, &count) in &ways {
            *next.entry(s + x).or_insert(0) += count;
            *next.entry(s - x).or_insert(0) += count;
        }
        ways = next;
    }
    ways.get(&target).copied().unwrap_or(0)
}

fn main() {
    println!("{:?}", find_target_sum_ways(vec![1, 1, 1, 1, 1], 3));
}
