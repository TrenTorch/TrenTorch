// O(rows * cols) time, O(cols) space
fn unique_paths_obstacles(grid: Vec<Vec<i64>>) -> i64 {
    let rows = grid.len();
    if rows == 0 {
        return 0;
    }
    let cols = grid[0].len();
    if cols == 0 {
        return 0;
    }
    const MOD: i64 = 1_000_000_007;
    let mut row = vec![0; cols];
    row[0] = if grid[0][0] == 0 { 1 } else { 0 };
    for r in 0..rows {
        for c in 0..cols {
            if grid[r][c] == 1 {
                row[c] = 0;
            } else if c > 0 {
                row[c] = (row[c] + row[c - 1]) % MOD;
            }
        }
    }
    row[cols - 1]
}

fn main() {
    println!("{:?}", unique_paths_obstacles(vec![vec![0, 0, 0], vec![0, 1, 0], vec![0, 0, 0]]));
}
