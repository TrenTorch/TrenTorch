// O(n) time, O(n) space
fn sorted_squares(nums: Vec<i64>) -> Vec<i64> {
    let n = nums.len();
    let mut out = vec![0; n];
    let mut left = 0;
    let mut right = n;
    if right > 0 {
        right -= 1;
    }
    for i in (0..n).rev() {
        if nums[left].abs() > nums[right].abs() {
            out[i] = nums[left] * nums[left];
            left += 1;
        } else {
            out[i] = nums[right] * nums[right];
            if right == 0 {
                break;
            }
            right -= 1;
        }
    }
    out
}

fn main() {
    println!("{:?}", sorted_squares(vec![-4, -1, 0, 3, 10]));
}
