// O(n) time, O(1) space
fn trap_water(heights: Vec<i64>) -> i64 {
    let mut left = 0;
    let mut right = heights.len().saturating_sub(1);
    let mut left_max = 0;
    let mut right_max = 0;
    let mut total = 0;

    while left < right {
        if heights[left] < heights[right] {
            left_max = left_max.max(heights[left]);
            total += left_max - heights[left];
            left += 1;
        } else {
            right_max = right_max.max(heights[right]);
            total += right_max - heights[right];
            right -= 1;
        }
    }

    total
}

fn main() {
    println!("{:?}", trap_water(vec![0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]));
}
