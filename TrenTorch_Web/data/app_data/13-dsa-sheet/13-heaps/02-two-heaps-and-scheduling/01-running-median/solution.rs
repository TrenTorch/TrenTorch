use std::collections::BinaryHeap;
use std::cmp::Reverse;

// O(n log n) time, O(n) space
fn running_median(nums: Vec<i64>) -> Vec<f64> {
    let mut low = BinaryHeap::new(); // max-heap for the lower half
    let mut high = BinaryHeap::new(); // min-heap (via Reverse) for the upper half
    let mut out = Vec::with_capacity(nums.len());

    for x in nums {
        low.push(x);
        if let Some(max_low) = low.pop() {
            high.push(Reverse(max_low));
        }
        if high.len() > low.len() {
            if let Some(Reverse(min_high)) = high.pop() {
                low.push(min_high);
            }
        }
        if low.len() > high.len() {
            out.push(*low.peek().unwrap() as f64);
        } else {
            let l = *low.peek().unwrap() as f64;
            let h = high.peek().unwrap().0 as f64;
            out.push((l + h) / 2.0);
        }
    }
    out
}

fn main() {
    println!("{:?}", running_median(vec![5, 15, 1, 3]));
}
