// O(n) time, O(1) space
fn next_typed(text: &[u8], mut i: isize) -> isize {
    let mut skip = 0;
    while i >= 0 {
        if text[i as usize] == b'#' {
            skip += 1;
        } else if skip > 0 {
            skip -= 1;
        } else {
            return i;
        }
        i -= 1;
    }
    -1
}

fn backspace_compare(s: String, t: String) -> bool {
    let s_bytes = s.as_bytes();
    let t_bytes = t.as_bytes();
    let mut i = s_bytes.len() as isize - 1;
    let mut j = t_bytes.len() as isize - 1;
    loop {
        i = next_typed(s_bytes, i);
        j = next_typed(t_bytes, j);
        if i < 0 && j < 0 {
            return true;
        }
        if i < 0 || j < 0 || s_bytes[i as usize] != t_bytes[j as usize] {
            return false;
        }
        i -= 1;
        j -= 1;
    }
}

fn main() {
    println!("{:?}", backspace_compare(String::from("ab#c"), String::from("ad#c")));
}
