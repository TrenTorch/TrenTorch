// O(rows * cols) time, O(cols) space
fn min_falling_path_sum(matrix: Vec<Vec<i64>>) -> i64 {
    if matrix.is_empty() || matrix[0].is_empty() {
        return 0;
    }
    let cols = matrix[0].len();
    let mut prev: Vec<i64> = matrix[0].clone();
    for r in 1..matrix.len() {
        let mut cur = vec![0i64; cols];
        for c in 0..cols {
            let lo = if c == 0 { 0 } else { c - 1 };
            let hi = std::cmp::min(c + 2, cols);
            let best = *prev[lo..hi].iter().min().unwrap();
            cur[c] = matrix[r][c] + best;
        }
        prev = cur;
    }
    *prev.iter().min().unwrap()
}

fn main() {
    println!("{:?}", min_falling_path_sum(vec![vec![2, 1, 3], vec![6, 5, 4], vec![7, 8, 9]]));
}
