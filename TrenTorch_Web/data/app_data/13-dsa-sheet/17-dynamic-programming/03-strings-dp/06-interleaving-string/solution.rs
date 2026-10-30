// O(len(a) * len(b)) time, O(len(b)) space
fn is_interleave(a: String, b: String, c: String) -> bool {
    let a = a.into_bytes();
    let b = b.into_bytes();
    let c = c.into_bytes();
    if a.len() + b.len() != c.len() {
        return false;
    }
    let mut row = vec![false; b.len() + 1];
    row[0] = true;
    for j in 1..=b.len() {
        row[j] = row[j - 1] && b[j - 1] == c[j - 1];
    }
    for i in 1..=a.len() {
        row[0] = row[0] && a[i - 1] == c[i - 1];
        for j in 1..=b.len() {
            row[j] = (row[j] && a[i - 1] == c[i + j - 1]) || (row[j - 1] && b[j - 1] == c[i + j - 1]);
        }
    }
    row[b.len()]
}

fn main() {
    println!("{:?}", is_interleave(String::from("aabcc"), String::from("dbbca"), String::from("aadbbcbcac")));
}
