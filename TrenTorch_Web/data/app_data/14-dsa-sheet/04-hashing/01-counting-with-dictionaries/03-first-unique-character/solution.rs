// O(n) time, O(1) space
fn first_unique_character(s: String) -> i64 {
    let bytes = s.as_bytes();
    let mut count = [0usize; 26];
    for &b in bytes {
        count[(b - b'a') as usize] += 1;
    }
    for (i, &b) in bytes.iter().enumerate() {
        if count[(b - b'a') as usize] == 1 {
            return i as i64;
        }
    }
    -1
}

fn main() {
    println!("{:?}", first_unique_character(String::from("leetcode")));
}
