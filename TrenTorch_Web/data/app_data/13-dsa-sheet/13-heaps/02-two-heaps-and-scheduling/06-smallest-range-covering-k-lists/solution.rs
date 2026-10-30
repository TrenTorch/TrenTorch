use std::collections::BinaryHeap;
use std::cmp::Reverse;

// O(N log k) time, O(k) space where N is total number of elements, k is number of lists
fn smallest_range(lists: Vec<Vec<i64>>) -> Vec<i64> {
    let k = lists.len();
    let mut heap = BinaryHeap::with_capacity(k);
    let mut current_max = i64::MIN;
    for (i, lst) in lists.iter().enumerate() {
        let val = lst[0];
        heap.push(Reverse((val, i, 0)));
        if val > current_max {
            current_max = val;
        }
    }
    let mut best_lo = heap.peek().unwrap().0 .0;
    let mut best_hi = current_max;
    while let Some(Reverse((value, i, j))) = heap.pop() {
        let range = current_max - value;
        let best_range = best_hi - best_lo;
        if range < best_range || (range == best_range && value < best_lo) {
            best_lo = value;
            best_hi = current_max;
        }
        if j + 1 == lists[i].len() {
            return vec![best_lo, best_hi];
        }
        let nxt = lists[i][j + 1];
        if nxt > current_max {
            current_max = nxt;
        }
        heap.push(Reverse((nxt, i, j + 1)));
    }
    vec![best_lo, best_hi]
}

fn main() {
    println!("{:?}", smallest_range(vec![vec![4, 10, 15, 24, 26], vec![0, 9, 12, 20], vec![5, 18, 22, 30]]));
}
