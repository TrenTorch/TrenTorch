fn erase_overlap(mut intervals: Vec<Vec<i64>>) -> i64 {
    // O(n log n) time, O(1) space
    intervals.sort_by_key(|v| v[1]);
    let mut removed = 0;
    let mut last_end = None;
    for interval in intervals {
        let start = interval[0];
        let end = interval[1];
        if last_end.is_none() || start >= last_end.unwrap() {
            last_end = Some(end);
        } else {
            removed += 1;
        }
    }
    removed
}

fn main() {
    println!("{:?}", erase_overlap(vec![vec![1, 2], vec![2, 3], vec![3, 4], vec![1, 3]]));
}
