// O(n) time, O(1) space
fn total_hamming_distance(nums: Vec<i64>) -> i64 {
    let n = nums.len();
    let mut total = 0i64;
    for i in 0..30 {
        let ones = nums.iter().filter(|&&x| (x >> i) & 1 == 1).count();
        total += (ones as i64) * ((n - ones) as i64);
    }
    total
}

fn main() {
    println!("{:?}", total_hamming_distance(vec![4, 14, 2]));
}
