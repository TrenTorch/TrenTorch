// O(n) time, O(1) space
fn longest_mountain(arr: Vec<i64>) -> i64 {
    let n = arr.len();
    let mut best: i64 = 0;
    let mut i: usize = 1;
    while i + 1 < n {
        if arr[i - 1] < arr[i] && arr[i] > arr[i + 1] {
            let mut left = i - 1;
            while left > 0 && arr[left - 1] < arr[left] {
                left -= 1;
            }
            let mut right = i + 1;
            while right + 1 < n && arr[right] > arr[right + 1] {
                right += 1;
            }
            best = best.max((right - left + 1) as i64);
            i = right + 1;
        } else {
            i += 1;
        }
    }
    best
}

fn main() {
    println!("{:?}", longest_mountain(vec![2, 1, 4, 7, 3, 2, 5]));
}
