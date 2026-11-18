use std::collections::HashSet;

fn neighbours(x: usize, y: usize, rows: usize, cols: usize) -> Vec<(usize, usize)> {
    let mut out = Vec::with_capacity(4);
    if x + 1 < rows {
        out.push((x + 1, y));
    }
    if x >= 1 {
        out.push((x - 1, y));
    }
    if y + 1 < cols {
        out.push((x, y + 1));
    }
    if y >= 1 {
        out.push((x, y - 1));
    }
    out
}

// O(R * C) time, O(R * C) space
fn largest_island(grid: Vec<Vec<i64>>) -> i64 {
    let rows = grid.len();
    let cols = if rows > 0 { grid[0].len() } else { 0 };
    let mut label = vec![vec![0usize; cols]; rows];
    // size[id] is the island size for label id; index 0 is a placeholder for "no island"
    let mut size: Vec<i64> = vec![0];
    let mut next_id = 1usize;
    for r in 0..rows {
        for c in 0..cols {
            if grid[r][c] == 1 && label[r][c] == 0 {
                label[r][c] = next_id;
                let mut stack = vec![(r, c)];
                let mut count: i64 = 0;
                while let Some((x, y)) = stack.pop() {
                    count += 1;
                    for (nx, ny) in neighbours(x, y, rows, cols) {
                        if grid[nx][ny] == 1 && label[nx][ny] == 0 {
                            label[nx][ny] = next_id;
                            stack.push((nx, ny));
                        }
                    }
                }
                size.push(count);
                next_id += 1;
            }
        }
    }
    let mut best: i64 = size.iter().skip(1).copied().max().unwrap_or(0);
    for r in 0..rows {
        for c in 0..cols {
            if grid[r][c] == 0 {
                let mut around: HashSet<usize> = HashSet::new();
                for (nx, ny) in neighbours(r, c, rows, cols) {
                    if label[nx][ny] != 0 {
                        around.insert(label[nx][ny]);
                    }
                }
                let total: i64 = 1 + around.iter().map(|&i| size[i]).sum::<i64>();
                best = best.max(total);
            }
        }
    }
    best
}

fn main() {
    println!("{:?}", largest_island(vec![vec![1, 0], vec![0, 1]]));
}
