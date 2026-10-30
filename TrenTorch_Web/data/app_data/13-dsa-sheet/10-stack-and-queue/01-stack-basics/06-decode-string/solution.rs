// O(L) time, O(L) space where L is length of decoded string
fn decode_string(s: String) -> String {
    let mut out: Vec<char> = Vec::new();
    let mut open_blocks: Vec<(usize, i64)> = Vec::new();
    let mut num: i64 = 0;

    for ch in s.chars() {
        if ch.is_ascii_digit() {
            num = num * 10 + (ch as i64 - '0' as i64);
        } else if ch == '[' {
            open_blocks.push((out.len(), num));
            num = 0;
        } else if ch == ']' {
            if let Some((start, count)) = open_blocks.pop() {
                if count == 0 {
                    out.truncate(start);
                } else if count > 1 {
                    let segment = out[start..].to_vec();
                    for _ in 1..count {
                        out.extend_from_slice(&segment);
                    }
                }
            }
        } else {
            out.push(ch);
        }
    }

    out.iter().collect()
}

fn main() {
    println!("{:?}", decode_string(String::from("3[a2[c]]")));
}
