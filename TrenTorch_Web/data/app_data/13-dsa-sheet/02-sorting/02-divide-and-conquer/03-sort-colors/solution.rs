// O(n) time, O(n) space
fn sort_colors(nums: Vec<i64>) -> Vec<i64> {
    let mut count0 = 0usize;
    let mut count1 = 0usize;
    let mut count2 = 0usize;
    for &v in &nums {
        match v {
            0 => count0 += 1,
            1 => count1 += 1,
            2 => count2 += 1,
            _ => {}
        }
    }
    let mut result = Vec::with_capacity(nums.len());
    result.extend(std::iter::repeat(0_i64).take(count0));
    result.extend(std::iter::repeat(1_i64).take(count1));
    result.extend(std::iter::repeat(2_i64).take(count2));
    result
}

fn main() {
    println!("{:?}", sort_colors(vec![2, 0, 2, 1, 1, 0]));
}
