// O(n) time, O(1) space
fn valid_palindrome(s: String) -> bool {
    let bytes = s.as_bytes();
    let mut i = 0usize;
    let mut j = if bytes.is_empty() { 0 } else { bytes.len() - 1 };
    while i < j {
        while i < j && !bytes[i].is_ascii_alphanumeric() {
            i += 1;
        }
        while i < j && !bytes[j].is_ascii_alphanumeric() {
            j -= 1;
        }
        if i >= j {
            break;
        }
        if bytes[i].to_ascii_lowercase() != bytes[j].to_ascii_lowercase() {
            return false;
        }
        i += 1;
        if j == 0 {
            break;
        }
        j -= 1;
    }
    true
}

fn main() {
    println!("{:?}", valid_palindrome(String::from("A man, a plan, a canal: Panama")));
}
