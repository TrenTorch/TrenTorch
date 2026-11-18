// O(log(rows * cols)) time, O(1) space
fn search_matrix(matrix: Vec<Vec<i64>>, target: i64) -> bool {
    if matrix.is_empty() || matrix[0].is_empty() {
        return false;
    }
    let rows = matrix.len();
    let cols = matrix[0].len();
    let mut lo: i64 = 0;
    let mut hi: i64 = (rows * cols) as i64 - 1;
    while lo <= hi {
        let mid = lo + (hi - lo) / 2;
        let value = matrix[(mid as usize) / cols][(mid as usize) % cols];
        if value == target {
            return true;
        }
        if value < target {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    false
}

fn main() {
    println!(
        "{:?}",
        search_matrix(
            vec![vec![1, 3, 5, 7], vec![10, 11, 16, 20], vec![23, 30, 34, 60]],
            3
        )
    );
}
