// O((len(nums) + len(queries)) * 30) time, O(len(nums) * 30) space
fn max_xor_queries(nums: Vec<i64>, queries: Vec<i64>) -> Vec<i64> {
    // Node 0 is the root and never a child, so 0 marks a missing child.
    let mut nodes: Vec<[usize; 2]> = vec![[0, 0]];
    for &n in &nums {
        let mut cur = 0usize;
        for b in (0..30).rev() {
            let bit = ((n >> b) & 1) as usize;
            if nodes[cur][bit] == 0 {
                nodes.push([0, 0]);
                let new_idx = nodes.len() - 1;
                nodes[cur][bit] = new_idx;
            }
            cur = nodes[cur][bit];
        }
    }

    let mut out = Vec::with_capacity(queries.len());
    for &x in &queries {
        let mut cur = 0usize;
        let mut best: i64 = 0;
        for b in (0..30).rev() {
            let bit = ((x >> b) & 1) as usize;
            let want = 1 - bit;
            if nodes[cur][want] != 0 {
                best |= 1i64 << b;
                cur = nodes[cur][want];
            } else {
                cur = nodes[cur][bit];
            }
        }
        out.push(best);
    }
    out
}

fn main() {
    println!("{:?}", max_xor_queries(vec![0, 1, 2, 3, 4], vec![3, 5]));
}
