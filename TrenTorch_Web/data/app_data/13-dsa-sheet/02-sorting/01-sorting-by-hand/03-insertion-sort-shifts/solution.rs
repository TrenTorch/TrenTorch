use std::collections::HashMap;

// O(n log n) time, O(n) space
fn insertion_sort_shifts(nums: Vec<i64>) -> i64 {
    // Coordinate compression
    let mut uniq = nums.clone();
    uniq.sort_unstable();
    uniq.dedup();

    let mut rank: HashMap<i64, usize> = HashMap::with_capacity(uniq.len());
    for (i, &v) in uniq.iter().enumerate() {
        rank.insert(v, i + 1); // 1‑based index for Fenwick tree
    }

    let size = uniq.len();
    let mut tree: Vec<i64> = vec![0; size + 1];
    let mut shifts: i64 = 0;

    for (seen, &x) in nums.iter().enumerate() {
        let idx = *rank.get(&x).unwrap();

        // query prefix sum (number of elements ≤ x seen so far)
        let mut i = idx;
        let mut not_bigger: i64 = 0;
        while i > 0 {
            not_bigger += tree[i];
            let lowbit = i & (!i + 1);
            i -= lowbit;
        }

        shifts += seen as i64 - not_bigger;

        // update tree: add current element
        let mut i = idx;
        while i <= size {
            tree[i] += 1;
            let lowbit = i & (!i + 1);
            i += lowbit;
        }
    }

    shifts
}

fn main() {
    println!("{:?}", insertion_sort_shifts(vec![3, 1, 2]));
}
