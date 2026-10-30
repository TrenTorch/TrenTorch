// O(sqrt(n)) time, O(log n) space (trial division by 2 and odd numbers)
fn prime_factors(mut n: i64) -> Vec<Vec<i64>> {
    let mut out: Vec<Vec<i64>> = Vec::new();
    let mut d: i64 = 2;
    while d * d <= n {
        if n % d == 0 {
            let mut e: i64 = 0;
            while n % d == 0 {
                n /= d;
                e += 1;
            }
            out.push(vec![d, e]);
        }
        d += if d == 2 { 1 } else { 2 };
    }
    if n > 1 {
        out.push(vec![n, 1]);
    }
    out
}

fn main() {
    println!("{:?}", prime_factors(360));
}
