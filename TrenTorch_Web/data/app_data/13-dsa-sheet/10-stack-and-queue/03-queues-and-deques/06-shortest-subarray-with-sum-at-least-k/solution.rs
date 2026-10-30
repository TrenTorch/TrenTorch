use std::collections::VecDeque;

// O(n) time, O(n) space
fn shortest_subarray_sum_k(nums: Vec<i64>, k: i64) -> i64 {
    let n = nums.len();
    let mut prefix: Vec<i64> = Vec::with_capacity(n + 1);
    prefix.push(0);
    for &x in &nums {
        let last = prefix[prefix.len() - 1];
        prefix.push(last + x);
    }
    let mut best: i64 = (n as i64) + 1;
    let mut window: VecDeque<usize> = VecDeque::new();
    for b in 0..prefix.len() {
        let p = prefix[b];
        while let Some(&front) = window.front() {
            if p - prefix[front] >= k {
                best = best.min((b as i64) - (front as i64));
                window.pop_front();
            } else {
                break;
            }
        }
        while let Some(&back) = window.back() {
            if prefix[back] >= p {
                window.pop_back();
            } else {
                break;
            }
        }
        window.push_back(b);
    }
    if best <= n as i64 {
        best
    } else {
        -1
    }
}

fn main() {
    println!("{:?}", shortest_subarray_sum_k(vec![2, -1, 2], 3));
}
