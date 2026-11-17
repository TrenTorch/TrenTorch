// O(n) time, O(1) space
fn wiggle_length(nums: Vec<i64>) -> i64 {
    if nums.is_empty() {
        return 0;
    }
    let mut length: i64 = 1;
    let mut direction: i64 = 0;
    for i in 1..nums.len() {
        let diff = nums[i] - nums[i - 1];
        if diff > 0 && direction <= 0 {
            length += 1;
            direction = 1;
        } else if diff < 0 && direction >= 0 {
            length += 1;
            direction = -1;
        }
    }
    length
}

fn main() {
    println!("{:?}", wiggle_length(vec![1, 7, 4, 9, 2, 5]));
}
