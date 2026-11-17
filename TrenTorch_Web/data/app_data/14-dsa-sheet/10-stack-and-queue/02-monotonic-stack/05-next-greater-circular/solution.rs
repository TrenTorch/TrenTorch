// O(n) time, O(n) space
fn next_greater_circular(nums: Vec<i64>) -> Vec<i64> {
    let n = nums.len();
    let mut out = vec![-1i64; n];
    let mut stack: Vec<usize> = Vec::new();
    for i in 0..(2 * n) {
        let x = nums[i % n];
        while let Some(&top) = stack.last() {
            if nums[top] < x {
                out[top] = x;
                stack.pop();
            } else {
                break;
            }
        }
        if i < n {
            stack.push(i);
        }
    }
    out
}

fn main() {
    println!("{:?}", next_greater_circular(vec![1, 2, 1]));
}
