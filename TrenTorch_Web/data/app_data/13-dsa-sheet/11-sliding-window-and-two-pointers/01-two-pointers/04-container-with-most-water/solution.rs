// O(n) time, O(1) space
fn max_water(heights: Vec<i64>) -> i64 {
    let mut left: usize = 0;
    let mut right: usize = heights.len().saturating_sub(1);
    let mut best: i64 = 0;
    while left < right {
        let h = heights[left].min(heights[right]);
        let area = h * ((right - left) as i64);
        best = best.max(area);
        if heights[left] < heights[right] {
            left += 1;
        } else {
            right -= 1;
        }
    }
    best
}

fn main() {
    println!("{:?}", max_water(vec![1, 8, 6, 2, 5, 4, 8, 3, 7]));
}
