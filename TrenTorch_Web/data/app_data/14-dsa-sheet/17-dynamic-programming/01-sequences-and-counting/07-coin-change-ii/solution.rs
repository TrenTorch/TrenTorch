// O(k * amount) time, O(amount) space (k = number of coins)
fn count_change(amount: i64, coins: Vec<i64>) -> i64 {
    const MODULUS: i64 = 1_000_000_007;
    let amt = amount as usize;
    let mut ways = vec![0i64; amt + 1];
    ways[0] = 1;
    for c in coins {
        let cu = c as usize;
        for a in cu..=amt {
            ways[a] = (ways[a] + ways[a - cu]) % MODULUS;
        }
    }
    ways[amt]
}

fn main() {
    println!("{:?}", count_change(5, vec![1, 2, 5]));
}
