// O(m·n) time, O(m·n) space
fn spiral_order(matrix: Vec<Vec<i64>>) -> Vec<i64> {
    if matrix.is_empty() || matrix[0].is_empty() {
        return Vec::new();
    }
    let rows = matrix.len() as i32;
    let cols = matrix[0].len() as i32;
    let mut out = Vec::with_capacity((rows * cols) as usize);
    let mut top: i32 = 0;
    let mut bottom: i32 = rows - 1;
    let mut left: i32 = 0;
    let mut right: i32 = cols - 1;

    while top <= bottom && left <= right {
        // top row
        for col in left..=right {
            out.push(matrix[top as usize][col as usize]);
        }
        // right column
        for row in (top + 1)..=bottom {
            out.push(matrix[row as usize][right as usize]);
        }
        // bottom row
        if top < bottom {
            for col in (left..right).rev() {
                out.push(matrix[bottom as usize][col as usize]);
            }
        }
        // left column
        if left < right {
            for row in ((top + 1)..bottom).rev() {
                out.push(matrix[row as usize][left as usize]);
            }
        }
        top += 1;
        bottom -= 1;
        left += 1;
        right -= 1;
    }

    out
}

fn main() {
    println!("{:?}", spiral_order(vec![vec![1, 2, 3], vec![4, 5, 6], vec![7, 8, 9]]));
}
