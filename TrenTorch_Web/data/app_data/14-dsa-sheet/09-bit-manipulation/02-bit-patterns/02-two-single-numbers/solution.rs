// O(n) time, O(1) space
fn two_single_numbers(nums: Vec<i64>) -> Vec<i64> {
    let mut xor_all: i64 = 0;
    for &x in &nums {
        xor_all ^= x;
    }
    let low: i64 = xor_all & (-xor_all);
    let mut a: i64 = 0;
    let mut b: i64 = 0;
    for &x in &nums {
        if (x & low) != 0 {
            a ^= x;
        } else {
            b ^= x;
        }
    }
    if a <= b {
        vec![a, b]
    } else {
        vec![b, a]
    }
}

fn main() {
    println!("{:?}", two_single_numbers(vec![1, 2, 1, 3, 2, 5]));
}
