// O(rows + cols) time, O(1) space
fn row_with_most_ones(matrix: Vec<Vec<i64>>) -> i64 {
    let mut best_row: i64 = -1;
    let mut col: usize = if matrix.is_empty() { 0 } else { matrix[0].len() };
    for (i, row) in matrix.iter().enumerate() {
        let mut moved = false;
        while col > 0 && row[col - 1] == 1 {
            col -= 1;
            moved = true;
        }
        if moved {
            best_row = i as i64;
        }
    }
    best_row
}

fn main() {
    println!(
        "{:?}",
        row_with_most_ones(vec![vec![0, 0, 1, 1], vec![0, 1, 1, 1], vec![0, 0, 0, 1]])
    );
}
