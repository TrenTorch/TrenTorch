use std::cmp::Reverse;
use std::collections::BinaryHeap;

// O(n log n) time, O(n) space
fn connect_ropes(ropes: Vec<i64>) -> i64 {
    let mut heap: BinaryHeap<Reverse<i64>> = ropes.into_iter().map(Reverse).collect();
    let mut total: i64 = 0;
    while heap.len() > 1 {
        let Reverse(a) = heap.pop().unwrap();
        let Reverse(b) = heap.pop().unwrap();
        let joined = a + b;
        total += joined;
        heap.push(Reverse(joined));
    }
    total
}

fn main() {
    println!("{:?}", connect_ropes(vec![4, 3, 2, 6]));
}
