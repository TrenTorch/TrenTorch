// O(m*n log(m*n)) time, O(m*n) space
fn minimum_effort_path(heights: Vec<Vec<i64>>) -> i64 {
    use std::cmp::Reverse;
    use std::collections::BinaryHeap;

    let rows = heights.len();
    let cols = heights[0].len();
    let mut effort = vec![vec![i64::MAX; cols]; rows];
    effort[0][0] = 0;

    let mut heap = BinaryHeap::new();
    heap.push(Reverse((0, 0, 0)));

    while let Some(Reverse((e, x, y))) = heap.pop() {
        if x == rows - 1 && y == cols - 1 {
            return e;
        }
        if e > effort[x][y] {
            continue;
        }
        let directions = [(1, 0), (-1, 0), (0, 1), (0, -1)];
        for (dx, dy) in directions {
            let nx = x as isize + dx;
            let ny = y as isize + dy;
            if nx >= 0 && nx < rows as isize && ny >= 0 && ny < cols as isize {
                let nx = nx as usize;
                let ny = ny as usize;
                let diff = (heights[nx][ny] - heights[x][y]).abs();
                let ne = e.max(diff);
                if ne < effort[nx][ny] {
                    effort[nx][ny] = ne;
                    heap.push(Reverse((ne, nx, ny)));
                }
            }
        }
    }
    0
}

fn main() {
    println!("{:?}", minimum_effort_path(vec![vec![1, 2, 2], vec![3, 8, 2], vec![5, 3, 5]]));
}
