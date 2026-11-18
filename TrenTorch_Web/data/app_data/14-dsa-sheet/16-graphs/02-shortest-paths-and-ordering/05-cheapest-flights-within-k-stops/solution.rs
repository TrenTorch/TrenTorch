// O(k * E) time, O(V) space
fn cheapest_price(n: i64, flights: Vec<Vec<i64>>, src: i64, dst: i64, k: i64) -> i64 {
    let n_usize = n as usize;
    let src_usize = src as usize;
    let dst_usize = dst as usize;
    let k_usize = k as usize;

    const INF: i64 = i64::MAX / 2;
    let mut best = vec![INF; n_usize];
    best[src_usize] = 0;

    for _ in 0..=k_usize {
        let mut nxt = best.clone();
        for flight in &flights {
            let a = flight[0] as usize;
            let b = flight[1] as usize;
            let price = flight[2];
            if best[a] != INF && best[a] + price < nxt[b] {
                nxt[b] = best[a] + price;
            }
        }
        best = nxt;
    }

    if best[dst_usize] == INF {
        -1
    } else {
        best[dst_usize]
    }
}

fn main() {
    println!("{:?}", cheapest_price(4, vec![vec![0, 1, 100], vec![1, 2, 100], vec![2, 0, 100], vec![1, 3, 600], vec![2, 3, 200]], 0, 3, 1));
}
