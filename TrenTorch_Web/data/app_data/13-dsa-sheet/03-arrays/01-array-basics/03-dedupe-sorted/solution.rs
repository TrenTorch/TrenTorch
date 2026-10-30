// O(n) time, O(n) space
fn dedupe_sorted(nums: Vec<i64>) -> Vec<i64> {
    let mut out = Vec::new();
    for x in nums {
        if out.last().map_or(true, |&last| last != x) {
            out.push(x);
        }
    }
    out
}

fn main() {
    println!("{:?}", dedupe_sorted(vec![1, 1, 2, 2, 2, 3]));
}
