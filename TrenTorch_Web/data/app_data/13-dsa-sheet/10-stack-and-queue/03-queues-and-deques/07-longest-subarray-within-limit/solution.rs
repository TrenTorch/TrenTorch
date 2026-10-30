use std::collections::VecDeque;

// O(n) time, O(n) space
fn longest_within_limit(nums: Vec<i64>, limit: i64) -> i64 {
    let mut big = VecDeque::new();
    let mut small = VecDeque::new();
    let mut left = 0;
    let mut best = 0;
    
    for right in 0..nums.len() {
        let x = nums[right];
        
        // Maintain big deque (decreasing order)
        while let Some(&back_idx) = big.back() {
            if nums[back_idx] <= x {
                big.pop_back();
            } else {
                break;
            }
        }
        big.push_back(right);
        
        // Maintain small deque (increasing order)
        while let Some(&back_idx) = small.back() {
            if nums[back_idx] >= x {
                small.pop_back();
            } else {
                break;
            }
        }
        small.push_back(right);
        
        // Shrink window if needed
        while nums[*big.front().unwrap()] - nums[*small.front().unwrap()] > limit {
            left += 1;
            if let Some(&front_idx) = big.front() {
                if front_idx < left {
                    big.pop_front();
                }
            }
            if let Some(&front_idx) = small.front() {
                if front_idx < left {
                    small.pop_front();
                }
            }
        }
        
        best = best.max(right - left + 1);
    }
    
    best as i64
}

fn main() {
    println!("{:?}", longest_within_limit(vec![8, 2, 4, 7], 4));
}
