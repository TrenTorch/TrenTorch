// O(n) time, O(n) space
fn sum_subarray_mins(arr: Vec<i64>) -> i64 {
    const MOD: i64 = 1_000_000_007;
    let n = arr.len();
    if n == 0 {
        return 0;
    }
    let mut left = vec![0i64; n];
    let mut right = vec![0i64; n];
    let mut stack: Vec<usize> = Vec::with_capacity(n);

    // previous less element (strictly less? Python uses >= for left, so left[i] is index of previous element < arr[i])
    for i in 0..n {
        while let Some(&top) = stack.last() {
            if arr[top] >= arr[i] {
                stack.pop();
            } else {
                break;
            }
        }
        left[i] = if stack.is_empty() { -1 } else { stack.last().copied().unwrap() as i64 };
        stack.push(i);
    }

    stack.clear();
    // next less or equal element (Python uses > for right, so right[i] is index of next element <= arr[i])
    for i in (0..n).rev() {
        while let Some(&top) = stack.last() {
            if arr[top] > arr[i] {
                stack.pop();
            } else {
                break;
            }
        }
        right[i] = if stack.is_empty() { n as i64 } else { stack.last().copied().unwrap() as i64 };
        stack.push(i);
    }

    let mut ans = 0i64;
    for i in 0..n {
        let left_count = (i as i64 - left[i]) % MOD;
        let right_count = (right[i] - i as i64) % MOD;
        let term = (arr[i] % MOD) * left_count % MOD * right_count % MOD;
        ans = (ans + term) % MOD;
    }
    ans
}

fn main() {
    println!("{:?}", sum_subarray_mins(vec![3, 1, 2, 4]));
}
