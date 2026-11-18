// O(rows * cols) time, O(rows * cols) space
fn transpose_matrix(matrix: Vec<Vec<i64>>) -> Vec<Vec<i64>> {
    if matrix.is_empty() || matrix[0].is_empty() {
        return Vec::new();
    }
    let rows = matrix.len();
    let cols = matrix[0].len();
    let mut result = vec![vec![0; rows]; cols];
    for i in 0..rows {
        for j in 0..cols {
            result[j][i] = matrix[i][j];
        }
    }
    result
}

fn main() {
    println!("{:?}", transpose_matrix(vec![vec![1, 2, 3], vec![4, 5, 6]]));
}
