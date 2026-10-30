// O(rows * cols) time, O(rows * cols) space
fn max_island_area(grid: Vec<Vec<i64>>) -> i64 {
    let rows = grid.len();
    if rows == 0 {
        return 0;
    }
    let cols = grid[0].len();
    if cols == 0 {
        return 0;
    }
    let mut seen = vec![vec![false; cols]; rows];
    let mut best = 0;
    for r in 0..rows {
        for c in 0..cols {
            if grid[r][c] == 1 && !seen[r][c] {
                seen[r][c] = true;
                let mut stack = vec![(r, c)];
                let mut size = 0;
                while let Some((x, y)) = stack.pop() {
                    size += 1;
                    for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
                        let nx = x as i64 + dx;
                        let ny = y as i64 + dy;
                        if nx >= 0 && nx < rows as i64 && ny >= 0 && ny < cols as i64 {
                            let nx = nx as usize;
                            let ny = ny as usize;
                            if grid[nx][ny] == 1 && !seen[nx][ny] {
                                seen[nx][ny] = true;
                                stack.push((nx, ny));
                            }
                        }
                    }
                }
                if size > best {
                    best = size;
                }
            }
        }
    }
    best
}

fn main() {
    println!("{:?}", max_island_area(vec![vec![1, 1, 0], vec![0, 1, 0], vec![0, 0, 1]]));
}
