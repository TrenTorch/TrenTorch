// O(n) time, O(1) extra space
fn max_subarray_range(nums: Vec<i64>) -> Vec<i64> {
    let n = nums.len();
    let mut best_sum = nums[0];
    let mut best_start: usize = 0;
    let mut best_end: usize = 0;
    let mut current_sum = nums[0];
    let mut begin: usize = 0;

    for i in 1..n {
        if current_sum < 0 {
            current_sum = nums[i];
            begin = i;
        } else {
            current_sum += nums[i];
        }

        if current_sum > best_sum {
            best_sum = current_sum;
            best_start = begin;
            best_end = i;
        }
    }

    vec![best_sum, best_start as i64, best_end as i64]
}

fn main() {
    println!("{:?}", max_subarray_range(vec![-2, 1, -3, 4, -1, 2, 1, -5, 4]));
}
