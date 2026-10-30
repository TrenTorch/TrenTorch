// O(n log M) time, O(1) space where M is max modulus
fn solve_congruences(remainders: Vec<i64>, moduli: Vec<i64>) -> i64 {
    let mut x = 0i64;
    let mut modulus = 1i64;
    for (r, m) in remainders.into_iter().zip(moduli.into_iter()) {
        let g = gcd(modulus, m);
        if (r - x) % g != 0 {
            return -1;
        }
        let lcm = modulus / g * m;
        let a = modulus / g;
        let b = m / g;
        let inv = mod_inv(a, b);
        let diff = (r - x) / g;
        let mut t = diff * inv;
        t %= b;
        if t < 0 {
            t += b;
        }
        x = (x + modulus * t) % lcm;
        if x < 0 {
            x += lcm;
        }
        modulus = lcm;
    }
    x
}

fn gcd(mut a: i64, mut b: i64) -> i64 {
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}

fn egcd(a: i64, b: i64) -> (i64, i64, i64) {
    if b == 0 {
        return (a, 1, 0);
    }
    let (g, x1, y1) = egcd(b, a % b);
    (g, y1, x1 - (a / b) * y1)
}

fn mod_inv(a: i64, m: i64) -> i64 {
    let (g, x, _) = egcd(a, m);
    debug_assert_eq!(g, 1);
    let mut inv = x % m;
    if inv < 0 {
        inv += m;
    }
    inv
}

fn main() {
    println!("{:?}", solve_congruences(vec![2, 3, 2], vec![3, 5, 7]));
}
