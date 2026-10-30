// O(n) expected time, O(n) space
fn kth_largest(nums: Vec<i64>, k: i64) -> i64 {
    let mut a = nums;
    let mut target: i64 = (a.len() as i64) - k;
    let mut seed: u64 = 0x9e3779b97f4a7c15;
    loop {
        seed = seed
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        let pivot = a[((seed >> 33) as usize) % a.len()];
        let less: Vec<i64> = a.iter().copied().filter(|&x| x < pivot).collect();
        let equal = a.iter().filter(|&&x| x == pivot).count() as i64;
        let less_len = less.len() as i64;
        if target < less_len {
            a = less;
        } else if target < less_len + equal {
            return pivot;
        } else {
            target -= less_len + equal;
            a = a.into_iter().filter(|&x| x > pivot).collect();
        }
    }
}

fn main() {
    println!("{:?}", kth_largest(vec![3, 2, 1, 5, 6, 4], 2));
}
