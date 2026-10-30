// O(m*n) time, O(m+n) space
fn set_matrix_zeroes(matrix: Vec<Vec<i64>>) -> Vec<Vec<i64>> {
    let rows = matrix.len();
    if rows == 0 {
        return Vec::new();
    }
    let cols = matrix[0].len();
    let mut row_zero = vec![false; rows];
    let mut col_zero = vec![false; cols];

    for i in 0..rows {
        for j in 0..cols {
            if matrix[i][j] == 0 {
                row_zero[i] = true;
                col_zero[j] = true;
            }
        }
    }

    let mut result = Vec::with_capacity(rows);
    for i in 0..rows {
        let mut new_row = Vec::with_capacity(cols);
        for j in 0..cols {
            if row_zero[i] || col_zero[j] {
                new_row.push(0);
            } else {
                new_row.push(matrix[i][j]);
            }
        }
        result.push(new_row);
    }
    result
}

fn main() {
    println!("{:?}", set_matrix_zeroes(vec![vec![1, 2, 3], vec![4, 0, 6], vec![7, 8, 9]]));
}
