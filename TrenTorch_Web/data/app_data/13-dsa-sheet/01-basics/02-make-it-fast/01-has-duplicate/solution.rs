// O(n) time, O(n) space
fn has_duplicate(nums: Vec<i64>) -> bool {
    use std::collections::HashSet;
    let mut seen = HashSet::new();
    for x in nums {
        if seen.contains(&x) {
            return true;
        }
        seen.insert(x);
    }
    false
}

fn main() {
    println!("{:?}", has_duplicate(vec![1, 2, 3, 1]));
}
