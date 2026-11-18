// O(n) time, O(1) space
fn check_sorted_rotated(nums: Vec<i64>) -> bool {
    let n = nums.len();
    if n == 0 {
        return true;
    }
    let mut drops = 0;
    for i in 0..n {
        let next = (i + 1) % n;
        if nums[i] > nums[next] {
            drops += 1;
            if drops > 1 {
                return false;
            }
        }
    }
    true
}

fn main() {
    println!("{:?}", check_sorted_rotated(vec![3, 4, 5, 1, 2]));
}
