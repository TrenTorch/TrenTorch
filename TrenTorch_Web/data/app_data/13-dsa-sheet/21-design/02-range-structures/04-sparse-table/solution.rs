// O(n log n) time and space to build, O(1) per query (sparse table)
fn range_minimums(nums: Vec<i64>, queries: Vec<Vec<i64>>) -> Vec<i64> {
    let n = nums.len();
    let mut table: Vec<Vec<i64>> = vec![nums];
    let mut k: usize = 1;
    while (1usize << k) <= n {
        let half = 1usize << (k - 1);
        let len = n - (1usize << k) + 1;
        let row: Vec<i64> = {
            let prev = &table[k - 1];
            (0..len)
                .map(|i| std::cmp::min(prev[i], prev[i + half]))
                .collect()
        };
        table.push(row);
        k += 1;
    }

    let mut out: Vec<i64> = Vec::with_capacity(queries.len());
    for q in queries.iter() {
        let left = q[0] as usize;
        let right = q[1] as usize;
        let length = right - left + 1;
        let level = length.ilog2() as usize;
        let offset = 1usize << level;
        let row = &table[level];
        out.push(std::cmp::min(row[left], row[right + 1 - offset]));
    }
    out
}

fn main() {
    println!("{:?}", range_minimums(vec![5, 2, 8, 1, 9], vec![vec![0, 4], vec![1, 2], vec![2, 2]]));
}
