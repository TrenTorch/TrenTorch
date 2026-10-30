// O(n log log n) time, O(n) space
fn count_primes(n: i64) -> i64 {
    if n < 3 {
        return 0;
    }
    let n_usize = n as usize;
    let mut sieve = vec![1u8; n_usize];
    sieve[0] = 0;
    sieve[1] = 0;
    let limit = (n_usize as f64).sqrt() as usize;
    for i in 2..=limit {
        if sieve[i] == 1 {
            let start = i * i;
            for j in (start..n_usize).step_by(i) {
                sieve[j] = 0;
            }
        }
    }
    sieve.iter().map(|&x| x as i64).sum()
}

fn main() {
    println!("{:?}", count_primes(10));
}
