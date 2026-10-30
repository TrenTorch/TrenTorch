use std::collections::BinaryHeap;

// O(n log n) time, O(n) space
fn last_stone_weight(stones: Vec<i64>) -> i64 {
    let mut heap: BinaryHeap<i64> = stones.into_iter().collect();
    while heap.len() > 1 {
        let a = heap.pop().unwrap();
        let b = heap.pop().unwrap();
        if a != b {
            heap.push(a - b);
        }
    }
    heap.pop().unwrap_or(0)
}

fn main() {
    println!("{:?}", last_stone_weight(vec![2, 7, 4, 1, 8, 1]));
}
