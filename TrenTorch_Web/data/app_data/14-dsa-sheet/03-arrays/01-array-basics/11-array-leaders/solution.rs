// O(n) time, O(n) space
fn array_leaders(nums: Vec<i64>) -> Vec<i64> {
    let mut out = Vec::new();
    let mut best: Option<i64> = None;
    for &x in nums.iter().rev() {
        if best.map_or(true, |b| x > b) {
            out.push(x);
            best = Some(x);
        }
    }
    out.reverse();
    out
}

fn main() {
    println!("{:?}", array_leaders(vec![16, 17, 4, 3, 5, 2]));
}
