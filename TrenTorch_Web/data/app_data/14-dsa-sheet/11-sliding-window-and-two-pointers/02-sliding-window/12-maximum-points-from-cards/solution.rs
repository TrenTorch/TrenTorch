// O(n) time, O(1) space
fn max_points(points: Vec<i64>, k: i64) -> i64 {
    let n = points.len();
    let size = n - k as usize;
    let mut window: i64 = points[..size].iter().sum();
    let mut smallest = window;
    for i in size..n {
        window += points[i] - points[i - size];
        smallest = smallest.min(window);
    }
    points.iter().sum::<i64>() - smallest
}

fn main() {
    println!("{:?}", max_points(vec![1, 2, 3, 4, 5, 6, 1], 3));
}
