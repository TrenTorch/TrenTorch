use std::collections::VecDeque;

// O(rows * cols) time, O(rows * cols) space
fn shortest_path_binary_matrix(grid: Vec<Vec<i64>>) -> i64 {
    let rows = grid.len();
    if rows == 0 {
        return -1;
    }
    let cols = grid[0].len();
    if cols == 0 {
        return -1;
    }
    if grid[0][0] == 1 || grid[rows - 1][cols - 1] == 1 {
        return -1;
    }

    let mut seen = vec![vec![false; cols]; rows];
    seen[0][0] = true;

    let mut queue = VecDeque::new();
    queue.push_back((0usize, 0usize, 1i64));

    let dirs = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ];

    while let Some((x, y, steps)) = queue.pop_front() {
        if x == rows - 1 && y == cols - 1 {
            return steps;
        }
        for (dx, dy) in dirs {
            let nx = x as i32 + dx;
            let ny = y as i32 + dy;
            if nx >= 0 && nx < rows as i32 && ny >= 0 && ny < cols as i32 {
                let ux = nx as usize;
                let uy = ny as usize;
                if grid[ux][uy] == 0 && !seen[ux][uy] {
                    seen[ux][uy] = true;
                    queue.push_back((ux, uy, steps + 1));
                }
            }
        }
    }

    -1
}

fn main() {
    println!("{:?}", shortest_path_binary_matrix(vec![vec![0, 0, 0], vec![1, 1, 0], vec![1, 1, 0]]));
}
