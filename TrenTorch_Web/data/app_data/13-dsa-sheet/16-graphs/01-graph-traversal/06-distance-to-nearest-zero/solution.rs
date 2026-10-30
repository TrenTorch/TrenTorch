use std::collections::VecDeque;

// O(rows * cols) time, O(rows * cols) space
fn nearest_zero(mat: Vec<Vec<i64>>) -> Vec<Vec<i64>> {
    let rows = mat.len();
    if rows == 0 {
        return Vec::new();
    }
    let cols = mat[0].len();
    let mut dist = vec![vec![-1; cols]; rows];
    let mut queue = VecDeque::new();

    for r in 0..rows {
        for c in 0..cols {
            if mat[r][c] == 0 {
                dist[r][c] = 0;
                queue.push_back((r, c));
            }
        }
    }

    let directions = [(1, 0), (-1, 0), (0, 1), (0, -1)];
    while let Some((x, y)) = queue.pop_front() {
        for (dx, dy) in directions {
            let nx = x as isize + dx;
            let ny = y as isize + dy;
            if nx >= 0 && nx < rows as isize && ny >= 0 && ny < cols as isize {
                let nx = nx as usize;
                let ny = ny as usize;
                if dist[nx][ny] == -1 {
                    dist[nx][ny] = dist[x][y] + 1;
                    queue.push_back((nx, ny));
                }
            }
        }
    }

    dist
}

fn main() {
    println!("{:?}", nearest_zero(vec![vec![0, 0, 0], vec![0, 1, 0], vec![1, 1, 1]]));
}
