// O(m*n) time, O(m*n) space
fn flood(heights: &[Vec<i64>], starts: &[(usize, usize)]) -> Vec<Vec<bool>> {
    let rows = heights.len();
    let cols = if rows > 0 { heights[0].len() } else { 0 };
    let mut visited = vec![vec![false; cols]; rows];
    let mut stack = Vec::new();
    for &(r, c) in starts {
        if !visited[r][c] {
            visited[r][c] = true;
            stack.push((r, c));
        }
    }
    while let Some((r, c)) = stack.pop() {
        let h = heights[r][c];
        if r > 0 && !visited[r - 1][c] && heights[r - 1][c] >= h {
            visited[r - 1][c] = true;
            stack.push((r - 1, c));
        }
        if r + 1 < rows && !visited[r + 1][c] && heights[r + 1][c] >= h {
            visited[r + 1][c] = true;
            stack.push((r + 1, c));
        }
        if c > 0 && !visited[r][c - 1] && heights[r][c - 1] >= h {
            visited[r][c - 1] = true;
            stack.push((r, c - 1));
        }
        if c + 1 < cols && !visited[r][c + 1] && heights[r][c + 1] >= h {
            visited[r][c + 1] = true;
            stack.push((r, c + 1));
        }
    }
    visited
}

fn pacific_atlantic(heights: Vec<Vec<i64>>) -> Vec<Vec<i64>> {
    let rows = heights.len();
    if rows == 0 {
        return Vec::new();
    }
    let cols = heights[0].len();
    if cols == 0 {
        return Vec::new();
    }

    let mut pacific_starts = Vec::new();
    for r in 0..rows {
        pacific_starts.push((r, 0));
    }
    for c in 0..cols {
        pacific_starts.push((0, c));
    }

    let mut atlantic_starts = Vec::new();
    for r in 0..rows {
        atlantic_starts.push((r, cols - 1));
    }
    for c in 0..cols {
        atlantic_starts.push((rows - 1, c));
    }

    let pacific_visited = flood(&heights, &pacific_starts);
    let atlantic_visited = flood(&heights, &atlantic_starts);

    let mut result = Vec::new();
    for r in 0..rows {
        for c in 0..cols {
            if pacific_visited[r][c] && atlantic_visited[r][c] {
                result.push(vec![r as i64, c as i64]);
            }
        }
    }
    result
}

fn main() {
    println!("{:?}", pacific_atlantic(vec![vec![1, 2], vec![2, 1]]));
}
