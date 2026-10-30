// O(n) time, O(n) space
fn compress_runs(s: String) -> String {
    let bytes = s.as_bytes();
    let mut result = String::with_capacity(s.len());
    let mut i = 0;
    while i < bytes.len() {
        let ch = bytes[i] as char;
        let mut count = 1usize;
        i += 1;
        while i < bytes.len() && bytes[i] == bytes[i - 1] {
            count += 1;
            i += 1;
        }
        result.push(ch);
        if count > 1 {
            result.push_str(&count.to_string());
        }
    }
    result
}

fn main() {
    println!("{:?}", compress_runs(String::from("aabcccccaaa")));
}
