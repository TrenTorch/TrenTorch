// O(n) time, O(1) space
fn single_number_ii(nums: Vec<i64>) -> i64 {
    let mut ones: i64 = 0;
    let mut twos: i64 = 0;
    for x in nums {
        ones = (ones ^ x) & !twos;
        twos = (twos ^ x) & !ones;
    }
    ones
}

fn main() {
    println!("{:?}", single_number_ii(vec![2, 2, 3, 2]));
}
