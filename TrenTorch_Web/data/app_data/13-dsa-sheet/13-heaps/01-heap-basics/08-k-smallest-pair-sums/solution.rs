use std::cmp::Reverse;
use std::collections::BinaryHeap;

// O(k log k) time, O(k) space
fn k_smallest_pair_sums(nums1: Vec<i64>, nums2: Vec<i64>, k: i64) -> Vec<i64> {
    if nums1.is_empty() || nums2.is_empty() || k <= 0 {
        return Vec::new();
    }
    let k = k as usize;
    let mut heap: BinaryHeap<Reverse<(i64, usize, usize)>> = (0..nums1.len().min(k))
        .map(|i| Reverse((nums1[i] + nums2[0], i, 0)))
        .collect();
    let mut out: Vec<i64> = Vec::new();
    while out.len() < k {
        let Some(Reverse((total, i, j))) = heap.pop() else {
            break;
        };
        out.push(total);
        if j + 1 < nums2.len() {
            heap.push(Reverse((nums1[i] + nums2[j + 1], i, j + 1)));
        }
    }
    out
}

fn main() {
    println!("{:?}", k_smallest_pair_sums(vec![1, 7, 11], vec![2, 4, 6], 3));
}
