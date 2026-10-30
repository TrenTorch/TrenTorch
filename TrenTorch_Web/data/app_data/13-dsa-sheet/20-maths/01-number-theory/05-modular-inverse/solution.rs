// O(log m) time, O(1) space
fn mod_inverse(a: i64, m: i64) -> i64 {
    if m == 1 {
        return 0;
    }
    let mut old_r = a % m;
    let mut r = m;
    let mut old_x = 1;
    let mut x = 0;
    while r != 0 {
        let q = old_r / r;
        let tmp_r = r;
        r = old_r - q * r;
        old_r = tmp_r;
        let tmp_x = x;
        x = old_x - q * x;
        old_x = tmp_x;
    }
    if old_r == 1 {
        let res = old_x % m;
        if res < 0 { res + m } else { res }
    } else {
        -1
    }
}

fn main() {
    println!("{:?}", mod_inverse(3, 11));
}
