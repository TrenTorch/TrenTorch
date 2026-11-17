// O(N log k) time, O(k) space where N is total number of elements
fn merge_k_arrays(arrays: Vec<Vec<i64>>) -> Vec<i64> {
    use std::collections::BinaryHeap;
    use std::cmp::Reverse;

    let mut heap = BinaryHeap::new();
    for (i, arr) in arrays.iter().enumerate() {
        if let Some(&first) = arr.first() {
            heap.push(Reverse((first, i, 0)));
        }
    }

    let mut out = Vec::new();
    while let Some(Reverse((value, i, j))) = heap.pop() {
        out.push(value);
        let next_j = j + 1;
        if next_j < arrays[i].len() {
            heap.push(Reverse((arrays[i][next_j], i, next_j)));
        }
    }
    out
}

fn main() {
    println!("{:?}", merge_k_arrays(vec![vec![1, 4, 5], vec![1, 3, 4], vec![2, 6]]));
}
