// O(rows * cols) time, O(rows * cols) space
fn flood_fill(mut image: Vec<Vec<i64>>, sr: i64, sc: i64, color: i64) -> Vec<Vec<i64>> {
    let (sr, sc) = (sr as usize, sc as usize);
    let old = image[sr][sc];
    if old == color {
        return image;
    }
    let rows = image.len();
    let cols = image[0].len();
    image[sr][sc] = color;
    let mut stack: Vec<(usize, usize)> = vec![(sr, sc)];
    while let Some((x, y)) = stack.pop() {
        let (x, y) = (x as isize, y as isize);
        for (nx, ny) in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)] {
            if nx >= 0 && (nx as usize) < rows && ny >= 0 && (ny as usize) < cols {
                let (ux, uy) = (nx as usize, ny as usize);
                if image[ux][uy] == old {
                    image[ux][uy] = color;
                    stack.push((ux, uy));
                }
            }
        }
    }
    image
}

fn main() {
    println!("{:?}", flood_fill(vec![vec![1, 1, 1], vec![1, 1, 0], vec![1, 0, 1]], 1, 1, 2));
}
