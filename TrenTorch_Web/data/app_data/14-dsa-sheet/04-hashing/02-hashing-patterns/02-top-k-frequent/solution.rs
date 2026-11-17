use std::collections::HashMap;

// O(n) expected time, O(d) space where d is the number of distinct values
fn top_k_frequent(nums: Vec<i64>, k: i64) -> Vec<i64> {
    let mut counts: HashMap<i64, i64> = HashMap::new();
    for v in nums {
        *counts.entry(v).or_insert(0) += 1;
    }
    let mut pairs: Vec<(i64, i64)> = counts
        .into_iter()
        .map(|(value, count)| (-count, value))
        .collect();
    if k <= 0 {
        return Vec::new();
    }
    if (k as usize) < pairs.len() {
        let mut chosen: Vec<(i64, i64)> = Vec::new();
        let mut pool = pairs;
        let mut need = k as usize;
        let mut seed: u64 = 0x9e3779b97f4a7c15;
        while need > 0 {
            seed = seed
                .wrapping_mul(6364136223846793005)
                .wrapping_add(1442695040888963407);
            let pivot = pool[((seed >> 33) as usize) % pool.len()];
            let less: Vec<(i64, i64)> = pool.iter().copied().filter(|&p| p < pivot).collect();
            if need <= less.len() {
                pool = less;
            } else if need == less.len() + 1 {
                chosen.extend(less);
                chosen.push(pivot);
                need = 0;
            } else {
                let taken = less.len() + 1;
                chosen.extend(less);
                chosen.push(pivot);
                need -= taken;
                pool = pool.into_iter().filter(|&p| p > pivot).collect();
            }
        }
        pairs = chosen;
    }
    pairs.sort();
    pairs.into_iter().map(|(_, value)| value).collect()
}

fn main() {
    println!("{:?}", top_k_frequent(vec![1, 1, 1, 2, 2, 3], 2));
}
