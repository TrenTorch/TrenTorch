// O(rows * cols) time, O(rows * cols) space
fn num_islands(grid: Vec<Vec<i64>>) -> i64 {
    let rows = grid.len();
    let cols = if rows == 0 { 0 } else { grid[0].len() };
    let mut seen = vec![vec![false; cols]; rows];
    let mut count = 0;

    for r in 0..rows {
        for c in 0..cols {
            if grid[r][c] == 1 && !seen[r][c] {
                count += 1;
                seen[r][c] = true;
                let mut stack = vec![(r, c)];
                while let Some((x, y)) = stack.pop() {
                    for (nx, ny) in [
                        (x + 1, y),
                        (x.wrapping_sub(1), y),
                        (x, y + 1),
                        (x, y.wrapping_sub(1)),
                    ] {
                        if nx < rows && ny < cols && grid[nx][ny] == 1 && !seen[nx][ny] {
                            seen[nx][ny] = true;
                            stack.push((nx, ny));
                        }
                    }
                }
            }
        }
    }
    count
}

fn main() {
    println!("{:?}", num_islands(vec![vec![1, 1, 0], vec![0, 1, 0], vec![0, 0, 1]]));
}
