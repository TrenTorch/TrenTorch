// O(max(len(a), len(b))) time, O(max(len(a), len(b))) space
fn add_binary(a: String, b: String) -> String {
    let a_bytes = a.as_bytes();
    let b_bytes = b.as_bytes();
    let mut out: Vec<u8> = Vec::new();
    let mut i: isize = a_bytes.len() as isize - 1;
    let mut j: isize = b_bytes.len() as isize - 1;
    let mut carry: u32 = 0;
    while i >= 0 || j >= 0 || carry > 0 {
        let mut total: u32 = carry;
        if i >= 0 {
            total += (a_bytes[i as usize] - b'0') as u32;
            i -= 1;
        }
        if j >= 0 {
            total += (b_bytes[j as usize] - b'0') as u32;
            j -= 1;
        }
        out.push(b'0' + (total % 2) as u8);
        carry = total / 2;
    }
    out.reverse();
    String::from_utf8(out).unwrap()
}

fn main() {
    println!("{:?}", add_binary(String::from("11"), String::from("1")));
}
