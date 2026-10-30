type Item = ((i64, i64, i64), Vec<i64>);

// O(n) average time (quickselect), O(n) space
fn k_closest(points: Vec<Vec<i64>>, k: i64) -> Vec<Vec<i64>> {
    if k <= 0 {
        return Vec::new();
    }
    let k = k as usize;
    let mut pool: Vec<Item> = points
        .into_iter()
        .map(|p| {
            let (x, y) = (p[0], p[1]);
            ((x * x + y * y, x, y), p)
        })
        .collect();
    if k < pool.len() {
        let mut chosen: Vec<Item> = Vec::new();
        let mut need = k;
        let mut seed: u64 = 0x9e37_79b9_7f4a_7c15;
        while need > 0 {
            seed ^= seed << 13;
            seed ^= seed >> 7;
            seed ^= seed << 17;
            let pivot = pool[(seed % pool.len() as u64) as usize].0;
            let mut less: Vec<Item> = Vec::new();
            let mut equal: Vec<Item> = Vec::new();
            let mut greater: Vec<Item> = Vec::new();
            for item in std::mem::take(&mut pool) {
                if item.0 < pivot {
                    less.push(item);
                } else if item.0 == pivot {
                    equal.push(item);
                } else {
                    greater.push(item);
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
                need -= less.len() + equal.len();
                chosen.extend(less);
                chosen.extend(equal);
                pool = greater;
            }
        }
        pool = chosen;
    }
    pool.sort_by_key(|item| item.0);
    pool.into_iter().map(|item| item.1).collect()
}

fn main() {
    println!("{:?}", k_closest(vec![vec![1, 3], vec![-2, 2]], 1));
}
