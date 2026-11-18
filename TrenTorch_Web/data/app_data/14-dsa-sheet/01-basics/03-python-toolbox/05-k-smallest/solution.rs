// O(n) expected time, O(n) space
fn k_smallest(nums: Vec<i64>, k: i64) -> Vec<i64> {
    if k <= 0 {
        return Vec::new();
    }
    if (k as usize) >= nums.len() {
        let mut all = nums;
        all.sort();
        return all;
    }
    let mut need = k as usize;
    let mut pool = nums;
    let mut chosen: Vec<i64> = Vec::new();
    let mut seed: u64 = 0x9e3779b97f4a7c15;
    while need > 0 {
        seed = seed
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        let pivot = pool[((seed >> 33) as usize) % pool.len()];
        let mut less: Vec<i64> = Vec::new();
        let mut equal: Vec<i64> = Vec::new();
        let mut greater: Vec<i64> = Vec::new();
        for &x in &pool {
            if x < pivot {
                less.push(x);
            } else if x == pivot {
                equal.push(x);
            } else {
                greater.push(x);
            }
        }
        if need <= less.len() {
            pool = less;
        } else if need <= less.len() + equal.len() {
            let take = need - less.len();
            chosen.extend(less);
            chosen.extend(equal.into_iter().take(take));
            need = 0;
        } else {
            let taken = less.len() + equal.len();
            chosen.extend(less);
            chosen.extend(equal);
            need -= taken;
            pool = greater;
        }
    }
    chosen.sort();
    chosen
}

fn main() {
    println!("{:?}", k_smallest(vec![7, 2, 9, 4, 2], 3));
}
