// O(n log n) time, O(n) space
fn job_scheduling(jobs: Vec<Vec<i64>>) -> i64 {
    let mut items: Vec<(i64, i64, i64)> = jobs.iter().map(|j| (j[0], j[1], j[2])).collect();
    items.sort_by_key(|j| j.1);
    let ends: Vec<i64> = items.iter().map(|j| j.1).collect();
    let n = items.len();
    let mut best = vec![0i64; n + 1];
    for i in 1..=n {
        let (start, _end, profit) = items[i - 1];
        // bisect_right(ends, start, 0, i - 1)
        let before = ends[..i - 1].partition_point(|&e| e <= start);
        best[i] = std::cmp::max(best[i - 1], profit + best[before]);
    }
    best[n]
}

fn main() {
    println!("{:?}", job_scheduling(vec![vec![1, 3, 50], vec![2, 4, 10], vec![3, 5, 40], vec![3, 6, 70]]));
}
