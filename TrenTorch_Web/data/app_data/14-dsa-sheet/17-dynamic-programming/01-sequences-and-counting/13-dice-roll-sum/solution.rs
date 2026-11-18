// O(dice * target) time, O(target) space
fn dice_ways(dice: i64, faces: i64, target: i64) -> i64 {
    const MOD: i64 = 1_000_000_007;
    let target_usize = target as usize;
    let faces_usize = faces as usize;
    let mut row = vec![0; target_usize + 1];
    row[0] = 1;
    for _ in 0..dice as usize {
        let mut prefix = vec![0; target_usize + 2];
        for t in 0..=target_usize {
            prefix[t + 1] = (prefix[t] + row[t]) % MOD;
        }
        let mut nxt = vec![0; target_usize + 1];
        for t in 1..=target_usize {
            let lower = if t > faces_usize { t - faces_usize } else { 0 };
            let val = (prefix[t] - prefix[lower]) % MOD;
            nxt[t] = if val < 0 { val + MOD } else { val };
        }
        row = nxt;
    }
    row[target_usize]
}

fn main() {
    println!("{:?}", dice_ways(2, 6, 7));
}
