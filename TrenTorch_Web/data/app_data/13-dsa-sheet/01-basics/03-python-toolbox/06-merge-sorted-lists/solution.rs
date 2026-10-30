// O(N log k) time, O(k) extra space where N is total elements and k is number of lists
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn merge_sorted_lists(lists: Vec<Vec<i64>>) -> Vec<i64> {
    let mut heap: BinaryHeap<(Reverse<i64>, usize, usize)> = BinaryHeap::new();

    for (list_idx, lst) in lists.iter().enumerate() {
        if let Some(&first) = lst.first() {
            heap.push((Reverse(first), list_idx, 0));
        }
    }

    let mut result = Vec::new();

    while let Some((Reverse(val), list_idx, elem_idx)) = heap.pop() {
        result.push(val);
        let next_idx = elem_idx + 1;
        if next_idx < lists[list_idx].len() {
            let next_val = lists[list_idx][next_idx];
            heap.push((Reverse(next_val), list_idx, next_idx));
        }
    }

    result
}

fn main() {
    println!("{:?}", merge_sorted_lists(vec![vec![1, 4, 7], vec![2, 5], vec![3, 6, 9]]));
}
