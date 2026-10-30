use std::collections::VecDeque;

// O(rows * cols) time, O(rows * cols) space
fn oranges_rotting(grid: Vec<Vec<i64>>) -> i64 {
    let rows = grid.len();
    let cols = if rows > 0 { grid[0].len() } else { 0 };
    let mut g = grid;
    let mut queue: VecDeque<(isize, isize)> = VecDeque::new();
    let mut fresh: i64 = 0;
    for r in 0..rows {
        for c in 0..cols {
            if g[r][c] == 2 {
                queue.push_back((r as isize, c as isize));
            } else if g[r][c] == 1 {
                fresh += 1;
            }
        }
    }
    let mut minutes: i64 = 0;
    while !queue.is_empty() && fresh > 0 {
        minutes += 1;
        let level = queue.len();
        for _ in 0..level {
            let (x, y) = queue.pop_front().unwrap();
            for (nx, ny) in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)] {
                if nx >= 0 && (nx as usize) < rows && ny >= 0 && (ny as usize) < cols {
                    let (ux, uy) = (nx as usize, ny as usize);
                    if g[ux][uy] == 1 {
                        g[ux][uy] = 2;
                        fresh -= 1;
                        queue.push_back((nx, ny));
                    }
                }
            }
        }
    }
    if fresh == 0 {
        minutes
    } else {
        -1
    }
}

fn main() {
    println!("{:?}", oranges_rotting(vec![vec![2, 1, 1], vec![1, 1, 0], vec![0, 1, 1]]));
}
