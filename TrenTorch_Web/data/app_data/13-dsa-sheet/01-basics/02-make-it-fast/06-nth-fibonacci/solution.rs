// O(log n) time, O(log n) space
fn nth_fibonacci(n: i64) -> i64 {
    fn fib(k: i64) -> (i128, i128) {
        if k == 0 {
            (0, 1)
        } else {
            let (a, b) = fib(k >> 1);
            let c = a * (2 * b - a);
            let d = a * a + b * b;
            if k & 1 == 1 {
                (d, c + d)
            } else {
                (c, d)
            }
        }
    }
    fib(n).0 as i64
}

fn main() {
    println!("{:?}", nth_fibonacci(10));
}
