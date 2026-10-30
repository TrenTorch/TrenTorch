// O(eggs * answer) time, O(eggs) space
fn egg_drop(eggs: i64, floors: i64) -> i64 {
    if floors == 0 || eggs == 0 {
        return 0;
    }
    let e = eggs as usize;
    let mut reach = vec![0i64; e + 1];
    let mut drops = 0i64;
    while reach[e] < floors {
        drops += 1;
        for i in (1..=e).rev() {
            reach[i] = reach[i - 1] + reach[i] + 1;
        }
    }
    drops
}

fn main() {
    println!("{:?}", egg_drop(2, 6));
}
