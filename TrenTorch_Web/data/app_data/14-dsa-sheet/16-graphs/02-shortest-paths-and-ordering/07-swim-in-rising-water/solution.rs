use std::cmp::Reverse;
use std::collections::BinaryHeap;

// O(R * C log(R * C)) time, O(R * C) space
fn swim_in_water(grid: Vec<Vec<i64>>) -> i64 {
    let n = grid.len();
    let m = grid[0].len();
    let mut seen = vec![vec![false; m]; n];
    let mut heap = BinaryHeap::new();
    heap.push(Reverse((grid[0][0], 0usize, 0usize)));
    seen[0][0] = true;
    while let Some(Reverse((t, x, y))) = heap.pop() {
        if x == n - 1 && y == m - 1 {
            return t;
        }
        let mut nbrs: Vec<(usize, usize)> = Vec::with_capacity(4);
        if x + 1 < n {
            nbrs.push((x + 1, y));
        }
        if x >= 1 {
            nbrs.push((x - 1, y));
        }
        if y + 1 < m {
            nbrs.push((x, y + 1));
        }
        if y >= 1 {
            nbrs.push((x, y - 1));
        }
        for (nx, ny) in nbrs {
            if !seen[nx][ny] {
                seen[nx][ny] = true;
                heap.push(Reverse((t.max(grid[nx][ny]), nx, ny)));
            }
        }
    }
    0
}

fn main() {
    println!("{:?}", swim_in_water(vec![vec![0, 2], vec![1, 3]]));
}
