// O(n log n) time, O(n) space (the sort)
fn min_arrows(points: Vec<Vec<i64>>) -> i64 {
    let mut sorted = points;
    sorted.sort_by_key(|p| p[1]);
    let mut arrows: i64 = 0;
    let mut arrow: Option<i64> = None;
    for p in &sorted {
        let (start, end) = (p[0], p[1]);
        match arrow {
            Some(a) if start <= a => {}
            _ => {
                arrows += 1;
                arrow = Some(end);
            }
        }
    }
    arrows
}

fn main() {
    println!("{:?}", min_arrows(vec![vec![10, 16], vec![2, 8], vec![1, 6], vec![7, 12]]));
}
