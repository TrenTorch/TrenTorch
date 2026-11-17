// O(log^3 n) time, O(1) space
fn is_prime(n: i64) -> bool {
    if n < 2 {
        return false;
    }
    let n_u64 = n as u64;
    let small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37];
    for &p in &small {
        if n_u64 % p == 0 {
            return n_u64 == p;
        }
    }
    let mut d = n_u64 - 1;
    let mut s = 0;
    while d % 2 == 0 {
        d /= 2;
        s += 1;
    }
    for &a in &small {
        let mut x = mod_pow(a, d, n_u64);
        if x == 1 || x == n_u64 - 1 {
            continue;
        }
        let mut found = false;
        for _ in 0..s - 1 {
            x = mod_mul(x, x, n_u64);
            if x == n_u64 - 1 {
                found = true;
                break;
            }
        }
        if !found {
            return false;
        }
    }
    true
}

fn mod_mul(a: u64, b: u64, m: u64) -> u64 {
    ((a as u128 * b as u128) % m as u128) as u64
}

fn mod_pow(mut base: u64, mut exp: u64, m: u64) -> u64 {
    let mut result = 1;
    while exp > 0 {
        if exp & 1 == 1 {
            result = mod_mul(result, base, m);
        }
        base = mod_mul(base, base, m);
        exp >>= 1;
    }
    result
}

fn main() {
    println!("{:?}", is_prime(97));
}
