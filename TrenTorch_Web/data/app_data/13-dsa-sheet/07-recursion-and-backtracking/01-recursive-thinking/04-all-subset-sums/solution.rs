// O(2^n) time, O(2^n) space
fn all_subset_sums(nums: Vec<i64>) -> Vec<i64> {
    let mut sums: Vec<i64> = vec![0];
    for x in nums {
        // both halves are sorted, so the sort on the merged list is cheap
        let mut merged: Vec<i64> = Vec::with_capacity(sums.len() * 2);
        merged.extend_from_slice(&sums);
        merged.extend(sums.iter().map(|s| s + x));
        merged.sort();
        sums = merged;
    }
    sums
}

fn main() {
    println!("{:?}", all_subset_sums(vec![1, 2]));
}
