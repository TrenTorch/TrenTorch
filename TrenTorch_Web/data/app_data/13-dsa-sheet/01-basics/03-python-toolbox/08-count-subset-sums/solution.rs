use std::collections::HashMap;

/// O(2^{n/2}) time, O(2^{n/2}) space
fn count_subset_sums(nums: Vec<i64>, k: i64, target: i64) -> i64 {
    fn sums_by_size(values: &[i64]) -> HashMap<(i64, i64), i64> {
        let mut states: HashMap<(i64, i64), i64> = HashMap::new();
        states.insert((0, 0), 1);
        for &v in values {
            // Snapshot current entries to avoid borrowing issues while mutating
            let current: Vec<((i64, i64), i64)> = states
                .iter()
                .map(|(&(size, sum), &ways)| ((size, sum), ways))
                .collect();
            for ((size, sum), ways) in current {
                let entry = states.entry((size + 1, sum + v)).or_insert(0);
                *entry += ways;
            }
        }
        states
    }

    let half = nums.len() / 2;
    let left = sums_by_size(&nums[..half]);
    let right = sums_by_size(&nums[half..]);

    let mut count: i64 = 0;
    for ((size_r, sum_r), ways_r) in right.iter() {
        let need_size = k - size_r;
        let need_sum = target - sum_r;
        if let Some(ways_l) = left.get(&(need_size, need_sum)) {
            count += ways_r * ways_l;
        }
    }
    count
}

fn main() {
    println!("{:?}", count_subset_sums(vec![1, 2, 3, 4], 2, 5));
}
