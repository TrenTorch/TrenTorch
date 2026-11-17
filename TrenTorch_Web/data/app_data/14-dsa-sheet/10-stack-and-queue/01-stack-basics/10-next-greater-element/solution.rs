// O(n) time, O(n) space
fn next_greater(nums: Vec<i64>) -> Vec<i64> {
    let n = nums.len();
    let mut out = vec![-1; n];
    let mut stack = Vec::new();
    
    for i in 0..n {
        while let Some(&top) = stack.last() {
            if nums[top] < nums[i] {
                out[stack.pop().unwrap()] = nums[i];
            } else {
                break;
            }
        }
        stack.push(i);
    }
    
    out
}

fn main() {
    println!("{:?}", next_greater(vec![2, 1, 2, 4, 3]));
}
