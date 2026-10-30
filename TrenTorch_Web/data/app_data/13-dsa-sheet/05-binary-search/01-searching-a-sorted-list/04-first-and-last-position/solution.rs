// O(log n) time, O(1) extra space
fn first_and_last(nums: Vec<i64>, target: i64) -> Vec<i64> {
    let n = nums.len();
    let mut lo: usize = 0;
    let mut hi: usize = n;
    while lo < hi {
        let mid = (lo + hi) / 2;
        if nums[mid] < target {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    if lo == n || nums[lo] != target {
        return vec![-1, -1];
    }
    let first = lo;
    lo = first;
    hi = n;
    while lo < hi {
        let mid = (lo + hi) / 2;
        if nums[mid] <= target {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    vec![first as i64, (lo - 1) as i64]
}

fn main() {
    println!("{:?}", first_and_last(vec![5, 7, 7, 8, 8, 10], 8));
}
