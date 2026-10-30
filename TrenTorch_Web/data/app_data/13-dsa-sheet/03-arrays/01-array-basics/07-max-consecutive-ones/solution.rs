// O(n) time, O(1) space
fn max_consecutive_ones(nums: Vec<i64>) -> i64 {
    let mut best: i64 = 0;
    let mut current: i64 = 0;
    for x in nums {
        if x == 1 {
            current += 1;
            best = best.max(current);
        } else {
            current = 0;
        }
    }
    best
}

fn main() {
    println!("{:?}", max_consecutive_ones(vec![1, 1, 0, 1, 1, 1]));
}
