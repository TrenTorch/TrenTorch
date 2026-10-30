// O(n) time, O(1) space
fn is_anagram(a: String, b: String) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut counts = [0i64; 26];
    for byte in a.bytes() {
        counts[(byte - b'a') as usize] += 1;
    }
    for byte in b.bytes() {
        counts[(byte - b'a') as usize] -= 1;
    }
    counts.iter().all(|&c| c == 0)
}

fn main() {
    println!("{:?}", is_anagram(String::from("listen"), String::from("silent")));
}
