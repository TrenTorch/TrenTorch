// O(sqrt(n)) time, O(1) space
fn num_squares(n: i64) -> i64 {
    if n == 0 {
        return 0;
    }
    let sqrt_n = (n as f64).sqrt() as i64;
    if sqrt_n * sqrt_n == n {
        return 1;
    }
    let mut m = n;
    while m % 4 == 0 {
        m /= 4;
    }
    if m % 8 == 7 {
        return 4;
    }
    let mut i = 1;
    while i * i <= n {
        let rest = n - i * i;
        let sqrt_rest = (rest as f64).sqrt() as i64;
        if sqrt_rest * sqrt_rest == rest {
            return 2;
        }
        i += 1;
    }
    3
}

fn main() {
    println!("{:?}", num_squares(12));
}
