// O(n) time, O(k) space
fn contains_nearby_duplicate(nums: Vec<i64>, k: i64) -> bool {
    use std::collections::HashSet;
    let mut window: HashSet<i64> = HashSet::new();
    let k_usize = if k < 0 { 0usize } else { k as usize };
    for (i, &x) in nums.iter().enumerate() {
        if window.contains(&x) {
            return true;
        }
        window.insert(x);
        if i >= k_usize {
            if let Some(&old) = nums.get(i - k_usize) {
                window.remove(&old);
            }
        }
    }
    false
}

fn main() {
    println!("{:?}", contains_nearby_duplicate(vec![1, 2, 3, 1], 3));
}
