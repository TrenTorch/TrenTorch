// O(rows * cols) time, O(cols) space
fn count_squares(matrix: Vec<Vec<i64>>) -> i64 {
    let rows = matrix.len();
    if rows == 0 {
        return 0;
    }
    let cols = matrix[0].len();
    let mut prev = vec![0; cols + 1];
    let mut total = 0;

    for r in 0..rows {
        let mut cur = vec![0; cols + 1];
        for c in 0..cols {
            if matrix[r][c] == 1 {
                cur[c + 1] = 1 + std::cmp::min(prev[c], std::cmp::min(prev[c + 1], cur[c]));
                total += cur[c + 1];
            }
        }
        prev = cur;
    }
    total
}

fn main() {
    println!("{:?}", count_squares(vec![vec![0, 1, 1, 1], vec![1, 1, 1, 1], vec![0, 1, 1, 1]]));
}
