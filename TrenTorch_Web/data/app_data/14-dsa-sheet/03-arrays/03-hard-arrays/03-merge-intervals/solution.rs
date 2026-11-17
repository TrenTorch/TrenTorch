// O(n log n) time, O(n) space
fn merge_intervals(intervals: Vec<Vec<i64>>) -> Vec<Vec<i64>> {
    let mut intervals = intervals;
    intervals.sort_by(|a, b| a[0].cmp(&b[0]));
    let mut out: Vec<Vec<i64>> = Vec::new();

    for intv in intervals {
        let start = intv[0];
        let end = intv[1];
        if let Some(last) = out.last_mut() {
            if start <= last[1] {
                if end > last[1] {
                    last[1] = end;
                }
            } else {
                out.push(vec![start, end]);
            }
        } else {
            out.push(vec![start, end]);
        }
    }

    out
}

fn main() {
    println!("{:?}", merge_intervals(vec![vec![1, 3], vec![8, 10], vec![2, 6], vec![15, 18]]));
}
