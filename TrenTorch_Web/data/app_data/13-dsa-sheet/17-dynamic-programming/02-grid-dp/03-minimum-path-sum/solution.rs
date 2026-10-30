// O(rows * cols) time, O(cols) space
fn min_path_sum(grid: Vec<Vec<i64>>) -> i64 {
    let rows = grid.len();
    if rows == 0 {
        return 0;
    }
    let cols = grid[0].len();
    if cols == 0 {
        return 0;
    }

    let mut row = vec![0i64; cols];
    for r in 0..rows {
        for c in 0..cols {
            if r == 0 && c == 0 {
                row[c] = grid[0][0];
            } else if r == 0 {
                row[c] = row[c - 1] + grid[r][c];
            } else if c == 0 {
                row[c] = row[c] + grid[r][c];
            } else {
                row[c] = row[c].min(row[c - 1]) + grid[r][c];
            }
        }
    }
    row[cols - 1]
}

fn main() {
    println!("{:?}", min_path_sum(vec![vec![1, 3, 1], vec![1, 5, 1], vec![4, 2, 1]]));
}
