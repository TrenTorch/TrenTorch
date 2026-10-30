// O(n^2) time, O(n) space
fn kth_permutation(n: i64, k: i64) -> String {
    let mut remaining: Vec<i64> = (1..=n).collect();
    let mut k = k - 1;
    let mut out = String::new();
    let mut size = n - 1;
    while size >= 0 {
        let block = factorial(size);
        let index = (k / block) as usize;
        k %= block;
        out.push_str(&remaining.remove(index).to_string());
        size -= 1;
    }
    out
}

fn factorial(m: i64) -> i64 {
    (1..=m).product()
}

fn main() {
    println!("{:?}", kth_permutation(3, 3));
}
