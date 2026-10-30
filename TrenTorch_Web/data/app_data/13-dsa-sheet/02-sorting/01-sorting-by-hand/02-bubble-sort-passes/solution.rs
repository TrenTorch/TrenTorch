// O(n log n) time, O(n) space
use std::collections::HashMap;

fn lowbit(x: usize) -> usize {
    x & (!x + 1)
}

fn bubble_sort_passes(nums: Vec<i64>) -> i64 {
    let n = nums.len();
    if n < 2 {
        return 1;
    }

    // coordinate compression
    let mut uniq = nums.clone();
    uniq.sort_unstable();
    uniq.dedup();

    let mut rank: HashMap<i64, usize> = HashMap::with_capacity(uniq.len());
    for (i, &v) in uniq.iter().enumerate() {
        rank.insert(v, i + 1); // 1‑based rank
    }

    let size = uniq.len();
    let mut bit = vec![0usize; size + 1];
    let mut most_bigger_before: i64 = 0;

    for (seen, &x) in nums.iter().enumerate() {
        let r = *rank.get(&x).unwrap();

        // query prefix sum: number of elements <= x seen so far
        let mut i = r;
        let mut not_bigger: i64 = 0;
        while i > 0 {
            not_bigger += bit[i] as i64;
            i -= lowbit(i);
        }

        let bigger_before = seen as i64 - not_bigger;
        if bigger_before > most_bigger_before {
            most_bigger_before = bigger_before;
        }

        // update BIT with current element
        let mut j = r;
        while j <= size {
            bit[j] += 1;
            j += lowbit(j);
        }
    }

    most_bigger_before + 1
}

fn main() {
    println!("{:?}", bubble_sort_passes(vec![3, 2, 1]));
}
