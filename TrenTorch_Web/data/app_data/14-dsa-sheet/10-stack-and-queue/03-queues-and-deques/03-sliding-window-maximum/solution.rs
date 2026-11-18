use std::collections::VecDeque;

// O(n) time, O(k) space
fn sliding_window_max(nums: Vec<i64>, k: i64) -> Vec<i64> {
    let mut window: VecDeque<usize> = VecDeque::new();
    let mut out: Vec<i64> = Vec::new();
    for i in 0..nums.len() {
        let x = nums[i];
        while let Some(&back) = window.back() {
            if nums[back] <= x {
                window.pop_back();
            } else {
                break;
            }
        }
        window.push_back(i);
        if (window[0] as i64) <= (i as i64) - k {
            window.pop_front();
        }
        if (i as i64) >= k - 1 {
            out.push(nums[window[0]]);
        }
    }
    out
}

fn main() {
    println!("{:?}", sliding_window_max(vec![1, 3, -1, -3, 5, 3, 6, 7], 3));
}
