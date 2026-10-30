// O(n^2) time, O(n) space
fn minimum_total(triangle: Vec<Vec<i64>>) -> i64 {
    if triangle.is_empty() {
        return 0;
    }
    let mut best = triangle.last().unwrap().clone();
    for row_idx in (0..triangle.len().saturating_sub(1)).rev() {
        let row = &triangle[row_idx];
        for j in 0..=row_idx {
            best[j] = row[j] + best[j].min(best[j + 1]);
        }
    }
    best[0]
}

fn main() {
    println!("{:?}", minimum_total(vec![vec![2], vec![3, 4], vec![6, 5, 7], vec![4, 1, 8, 3]]));
}
