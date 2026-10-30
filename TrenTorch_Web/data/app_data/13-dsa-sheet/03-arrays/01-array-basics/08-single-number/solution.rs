// O(n) time, O(1) space
fn single_number(nums: Vec<i64>) -> i64 {
    nums.iter().fold(0, |acc, &x| acc ^ x)
}

fn main() {
    println!("{:?}", single_number(vec![4, 1, 2, 1, 2]));
}
