// O(sqrt(n)) time, O(1) space
fn euler_phi(n: i64) -> i64 {
    let mut result = n;
    let mut n = n;
    let mut d = 2;
    while d * d <= n {
        if n % d == 0 {
            while n % d == 0 {
                n /= d;
            }
            result -= result / d;
        }
        d += if d == 2 { 1 } else { 2 };
    }
    if n > 1 {
        result -= result / n;
    }
    result
}

fn main() {
    println!("{:?}", euler_phi(12));
}
