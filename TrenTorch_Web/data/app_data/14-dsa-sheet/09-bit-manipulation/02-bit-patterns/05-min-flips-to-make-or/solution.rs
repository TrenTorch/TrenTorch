// O(1) time, O(1) space
fn min_flips(a: i64, b: i64, c: i64) -> i64 {
    let mut flips = 0;
    for i in 0..31 {
        let x = (a >> i) & 1;
        let y = (b >> i) & 1;
        let z = (c >> i) & 1;
        if z == 0 {
            flips += x + y;
        } else if x == 0 && y == 0 {
            flips += 1;
        }
    }
    flips
}

fn main() {
    println!("{:?}", min_flips(2, 6, 5));
}
