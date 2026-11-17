use std::cmp::Reverse;
use std::collections::BinaryHeap;

// O((n + m) log k) time, O(k) space
fn kth_largest_stream(k: i64, nums: Vec<i64>, adds: Vec<i64>) -> Vec<i64> {
    let k = k as usize;
    let mut heap: BinaryHeap<Reverse<i64>> = BinaryHeap::new();
    for x in nums {
        heap.push(Reverse(x));
        if heap.len() > k {
            heap.pop();
        }
    }
    let mut out: Vec<i64> = Vec::with_capacity(adds.len());
    for x in adds {
        if heap.len() < k {
            heap.push(Reverse(x));
        } else {
            heap.push(Reverse(x));
            heap.pop();
        }
        out.push(heap.peek().unwrap().0);
    }
    out
}

fn main() {
    println!("{:?}", kth_largest_stream(3, vec![4, 5, 8, 2], vec![3, 5, 10, 9, 4]));
}
