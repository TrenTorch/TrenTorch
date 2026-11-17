// O(n) time, O(n) space
fn nth_ugly_number(n: i64) -> i64 {
    let n = n as usize;
    let mut ugly: Vec<i64> = vec![1];
    let (mut i2, mut i3, mut i5) = (0usize, 0usize, 0usize);
    while ugly.len() < n {
        let nxt = (ugly[i2] * 2).min(ugly[i3] * 3).min(ugly[i5] * 5);
        ugly.push(nxt);
        if nxt == ugly[i2] * 2 {
            i2 += 1;
        }
        if nxt == ugly[i3] * 3 {
            i3 += 1;
        }
        if nxt == ugly[i5] * 5 {
            i5 += 1;
        }
    }
    ugly[n - 1]
}

fn main() {
    println!("{:?}", nth_ugly_number(10));
}
