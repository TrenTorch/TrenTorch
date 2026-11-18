// O(rows * cols) time, O(cols) space
fn maximal_rectangle(matrix: Vec<Vec<i64>>) -> i64 {
    if matrix.is_empty() {
        return 0;
    }
    let cols = matrix[0].len();
    let mut heights = vec![0; cols];
    let mut best = 0;

    for row in matrix {
        for j in 0..cols {
            if row[j] == 1 {
                heights[j] += 1;
            } else {
                heights[j] = 0;
            }
        }
        let area = largest_rectangle_histogram(&heights);
        if area > best {
            best = area;
        }
    }
    best
}

fn largest_rectangle_histogram(heights: &[i64]) -> i64 {
    let mut stack = Vec::new();
    let mut max_area = 0;
    for i in 0..=heights.len() {
        let h = if i == heights.len() { 0 } else { heights[i] };
        while let Some(&top) = stack.last() {
            if heights[top] >= h {
                let height = heights[stack.pop().unwrap()];
                let left = stack.last().copied().map(|x| x as i64).unwrap_or(-1);
                let width = i as i64 - left - 1;
                let area = height * width;
                if area > max_area {
                    max_area = area;
                }
            } else {
                break;
            }
        }
        stack.push(i);
    }
    max_area
}

fn main() {
    println!("{:?}", maximal_rectangle(vec![vec![1, 0, 1, 0, 0], vec![1, 0, 1, 1, 1], vec![1, 1, 1, 1, 1], vec![1, 0, 0, 1, 0]]));
}
