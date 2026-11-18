use std::cmp::Reverse;
use std::collections::BinaryHeap;

// O(n log k) time, O(k) space
fn sort_k_sorted(nums: Vec<i64>, k: i64) -> Vec<i64> {
    let k = k as usize;
    let mut heap: BinaryHeap<Reverse<i64>> =
        nums.iter().take(k + 1).map(|&x| Reverse(x)).collect();
    let mut out: Vec<i64> = Vec::with_capacity(nums.len());
    for &x in nums.iter().skip(k + 1) {
        heap.push(Reverse(x));
        let Reverse(smallest) = heap.pop().unwrap();
        out.push(smallest);
    }
    while let Some(Reverse(v)) = heap.pop() {
        out.push(v);
    }
    out
}

fn main() {
    println!("{:?}", sort_k_sorted(vec![6, 5, 3, 2, 8, 10, 9], 3));
}
