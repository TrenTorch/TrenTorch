fn is_pal_range(bytes: &[u8], mut i: usize, mut j: usize) -> bool {
    while i < j {
        if bytes[i] != bytes[j] {
            return false;
        }
        i += 1;
        j -= 1;
    }
    true
}

// O(n) time, O(1) extra space
fn valid_palindrome_ii(s: String) -> bool {
    let bytes = s.as_bytes();
    let n = bytes.len();
    let mut i: usize = 0;
    let mut j: usize = n.saturating_sub(1);
    while i < j {
        if bytes[i] != bytes[j] {
            return is_pal_range(bytes, i + 1, j) || is_pal_range(bytes, i, j - 1);
        }
        i += 1;
        j -= 1;
    }
    true
}

fn main() {
    println!("{:?}", valid_palindrome_ii(String::from("aba")));
}
