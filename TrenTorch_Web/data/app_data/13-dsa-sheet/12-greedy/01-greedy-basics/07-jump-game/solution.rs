// O(n) time, O(1) space
fn can_jump(nums: Vec<i64>) -> bool {
    let mut far: i64 = 0;
    for (i, &jump) in nums.iter().enumerate() {
        let i = i as i64;
        if i > far {
            return false;
        }
        far = far.max(i + jump);
    }
    true
}

fn main() {
    println!("{:?}", can_jump(vec![2, 3, 1, 1, 4]));
}
