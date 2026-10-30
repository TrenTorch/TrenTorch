// O(rows * cols) time, O(rows * cols) space
fn rotate_matrix(matrix: Vec<Vec<i64>>) -> Vec<Vec<i64>> {
    if matrix.is_empty() || matrix[0].is_empty() {
        return Vec::new();
    }
    let rows = matrix.len();
    let cols = matrix[0].len();
    let mut out: Vec<Vec<i64>> = Vec::with_capacity(cols);
    for c in 0..cols {
        let mut line: Vec<i64> = Vec::with_capacity(rows);
        for r in (0..rows).rev() {
            line.push(matrix[r][c]);
        }
        out.push(line);
    }
    out
}

fn main() {
    println!("{:?}", rotate_matrix(vec![vec![1, 2, 3], vec![4, 5, 6]]));
}
