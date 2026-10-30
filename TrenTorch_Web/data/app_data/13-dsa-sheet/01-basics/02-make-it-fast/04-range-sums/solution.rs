// O(n + m) time, O(n) space
fn range_sums(nums: Vec<i64>, queries: Vec<Vec<i64>>) -> Vec<i64> {
    let n = nums.len();
    let mut prefix = Vec::with_capacity(n + 1);
    prefix.push(0);
    for &val in &nums {
        let last = *prefix.last().unwrap();
        prefix.push(last + val);
    }

    let mut results = Vec::with_capacity(queries.len());
    for q in queries {
        let left = q[0] as usize;
        let right = q[1] as usize;
        let sum = prefix[right + 1] - prefix[left];
        results.push(sum);
    }
    results
}

fn main() {
    println!("{:?}", range_sums(vec![1, 2, 3, 4, 5], vec![vec![0, 4], vec![1, 3], vec![2, 2]]));
}
