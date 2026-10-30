use std::collections::{HashMap, BinaryHeap};
use std::cmp::Reverse;

// O(n log n) time, O(n) space
fn is_n_straight_hand(hand: Vec<i64>, group_size: i64) -> bool {
    if hand.len() % group_size as usize != 0 {
        return false;
    }
    let mut count = HashMap::new();
    for &x in &hand {
        *count.entry(x).or_insert(0) += 1;
    }
    let mut heap = BinaryHeap::new();
    for &k in count.keys() {
        heap.push(Reverse(k));
    }
    while !heap.is_empty() {
        let start = heap.peek().unwrap().0;
        for x in start..start + group_size {
            let cnt = match count.get_mut(&x) {
                Some(c) => c,
                None => return false,
            };
            if *cnt == 0 {
                return false;
            }
            *cnt -= 1;
            if *cnt == 0 {
                if x != heap.peek().unwrap().0 {
                    return false;
                }
                heap.pop();
            }
        }
    }
    true
}

fn main() {
    println!("{:?}", is_n_straight_hand(vec![1, 2, 3, 6, 2, 3, 4, 7, 8], 3));
}
