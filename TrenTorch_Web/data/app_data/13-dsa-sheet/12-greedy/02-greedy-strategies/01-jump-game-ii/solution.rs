// O(n) time, O(1) space
fn min_jumps(nums: Vec<i64>) -> i64 {
    let n = nums.len();
    if n <= 1 {
        return 0;
    }
    let mut jumps: i64 = 0;
    let mut end: usize = 0;
    let mut far: usize = 0;
    for i in 0..n - 1 {
        far = far.max(i + nums[i] as usize);
        if i == far {
            return -1;
        }
        if i == end {
            jumps += 1;
            end = far;
            if end >= n - 1 {
                break;
            }
        }
    }
    if end >= n - 1 {
        jumps
    } else {
        -1
    }
}

fn main() {
    println!("{:?}", min_jumps(vec![2, 3, 1, 1, 4]));
}
