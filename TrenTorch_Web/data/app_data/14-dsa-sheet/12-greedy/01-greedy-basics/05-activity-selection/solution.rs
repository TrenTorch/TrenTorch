// O(n log n) time, O(n) space
fn max_activities(starts: Vec<i64>, ends: Vec<i64>) -> i64 {
    let mut activities: Vec<(i64, i64)> = ends.into_iter().zip(starts.into_iter()).collect();
    activities.sort();
    let mut count = 0;
    let mut last_end = -1;
    for &(end, start) in &activities {
        if start >= last_end {
            count += 1;
            last_end = end;
        }
    }
    count
}

fn main() {
    println!("{:?}", max_activities(vec![1, 3, 0, 5, 8, 5], vec![2, 4, 6, 7, 9, 9]));
}
