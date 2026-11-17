// O(n * A(n)) time where A(n) is the answer size (about 1.6^n), O(n) extra space
fn no_adjacent_ones(n: i64) -> Vec<String> {
    let n = n as usize;
    let mut out: Vec<String> = Vec::new();
    let mut prefix = String::new();
    binary_go(n, &mut prefix, &mut out);
    out
}

fn binary_go(n: usize, prefix: &mut String, out: &mut Vec<String>) {
    if prefix.len() == n {
        out.push(prefix.clone());
        return;
    }
    prefix.push('0');
    binary_go(n, prefix, out);
    prefix.pop();
    if !prefix.ends_with('1') {
        prefix.push('1');
        binary_go(n, prefix, out);
        prefix.pop();
    }
}

fn main() {
    println!("{:?}", no_adjacent_ones(3));
}
